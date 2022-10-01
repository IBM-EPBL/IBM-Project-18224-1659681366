# for ibm
import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=764264db-9824-4b7c-82df-40d1b13897c2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32536;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=hhn68702;PWD=JDmq4keRKWs2f0Mi", '', '')
# end of ibm

query = "SELECT * FROM STUDENT WHERE FIRSTNAME='Karthikeyan'"
exe_cute = ibm_db.prepare(conn,query)

ibm_db.execute(exe_cute)

city = ibm_db.fetch_assoc(exe_cute)

city  = ibm_db.result(exe_cute,'CITY')

print("The Name is : ",city)

# while data!=False:
#     print("The Name is : ",city)
#     print(" ************ *****  ***** ")
    