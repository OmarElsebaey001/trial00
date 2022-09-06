import re 
def get_meta_from_contract(contract_cont):
    contract_note_no = re.findall("Contract Note No.*?:(.*)",contract_cont)[0]
    trade_date = re.findall ("TRADE DATE\s*?:\s*(\d{2}-\d{2}-\d{4}).*",contract_cont)[0]
    settlemnt_no = re.findall ("SETTLEMENT NO.\s(\d*).*",contract_cont)[0]
    settlement_date = re.findall ("SETTLEMENT DATE.*:\s*(\d{2}-\d{2}-\d{4}).*",contract_cont)[0]
    mob_num = re.findall ("Mob No:\s*(\d*).*",contract_cont)[0]
    ucc_no = re.findall("UCC of Client\s*:\s*(\d*)",contract_cont)[0]
    pan_of_client = re.findall ("PAN of Client\s*:\s*(.*)",contract_cont)[0]
    meta_contract = [contract_note_no,trade_date,settlemnt_no,settlement_date,mob_num,ucc_no,pan_of_client]
    return meta_contract
def seperate_table_from_contract(contract_cont):
    seperate_table = re.findall("Order No.*?Total Payable / Receivable.*?\n",contract_cont,re.DOTALL)
    return seperate_table
def extract_transaction_from_table(seperated_table):
    transactions=[]
    for table in seperated_table:       
        transaction_table  = re.findall("\d+\s+\d+\s+\d+\s+[\d{2}:\d{2}].*",table) 
               
        for record in transaction_table :
            records_list = record.split()
            name = " ".join(records_list[5:len(records_list)-6])
            del records_list[5:len(records_list)-6]
            records_list.insert(5,name)
            transactions.append(records_list)
    return transactions
def extract_meta_from_table (seperated_table):
    meta_detailed_table = []
    for table in seperated_table:
        meta = re.findall("(?:Buy|Sell|Total Payable.*?)(\s+\d+\s+\d+\.\d+\s+\d+\.\d+\s+\d+\.\d+\s+\d+\.\d+\s+\d+\.\d+\s+\d+\.\d+.*)\n",table)
        meta_data = [i.split() for i in meta]
        meta_detailed_table.append(meta_data)
    return meta_detailed_table
def get_detailed_table (seperated_table):
    get_transaction = extract_transaction_from_table(seperated_table)
    get_meta = extract_meta_from_table(seperated_table)
    return (get_transaction,get_meta)

def seperate_summary_table (contract_cont):
    summary_table_str = re.search("Transaction settled by delivery-Purchase.*Securities Transaction Tax .*?\n",contract_cont,re.DOTALL)[0]
    return summary_table_str

def extract_meta_summary_table(summary_table):
    total_meta_summary = re.findall("TOTAL.*\s+(\d+\.\d+).*",summary_table)[0]
    securties_meta_summary = re.findall("Securities Transaction Tax.*\s+(\d+\.\d+).*",summary_table)[0]
    return total_meta_summary,securties_meta_summary

def exract_transactin_summary_table (summary_table):
    transacton_summary_table = re.findall(".*\d+\s\d+\.\d+\s+\d+\.\d+",summary_table)
    records = [i.split() for i in transacton_summary_table]
    return records

def extract_summary_table(summary_table):
    meta_summary = extract_meta_summary_table(summary_table)
    transaction_summary = exract_transactin_summary_table(summary_table)
    return (transaction_summary,meta_summary)

def get_data_from_contract (contract_path):
    contract_handler = open (contract_path,"r")
    contract_content = contract_handler.read()
    meta_contract = get_meta_from_contract(contract_content)
    seperate_detailed_table = seperate_table_from_contract(contract_content)
    detailed_table = get_detailed_table(seperate_detailed_table)
    seperated_summary_table = seperate_summary_table(contract_content)
    summary_table = extract_summary_table(seperated_summary_table)
    final_res = [meta_contract,detailed_table,summary_table]
    return final_res