import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://bugngjsujrfafg:d240a665a22702b1584ce54a4feac539c17acd6d43bc45f1254e5e2146f8e46b@ec2-3-222-30-53.compute-1.amazonaws.com:5432/dbe6r5dcikh4di")
db = scoped_session(sessionmaker(bind=engine))


def main():
    db.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, first_name VARCHAR NOT NULL, last_name VARCHAR NOT NULL, country VARCHAR NOT NULL, username VARCHAR NOT NULL, password VARCHAR NOT NULL, gender VARCHAR NOT NULL)")
    db.execute("CREATE TABLE reviews (isbn VARCHAR NOT NULL,review VARCHAR NOT NULL, rating INTEGER NOT NULL,username VARCHAR NOT NULL)")
    db.execute("CREATE TABLE books (isbn VARCHAR PRIMARY KEY,title VARCHAR NOT NULL,author VARCHAR NOT NULL,year VARCHAR NOT NULL)")
    f=open("books.csv")
    reader =csv.reader(f)
    for isbn,title,author,year in reader:    
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:a,:b,:c,:d)",{"a":isbn,"b":title,"c":author,"d":year})
        
    print("done")            
    db.commit()    

if __name__ == "__main__":
    main()