#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
import time
import sqlite3
import re


# In[2]:


try:
    conobj=sqlite3.connect(database="bank.sqlite")
    curobj=conobj.cursor()
    curobj.execute("create table acn(acn_no integer primary key autoincrement,acn_name text,acn_email text,acn_mob text,acn_pass text,acn_gender text,acn_opendate text,acn_bal float)")
    conobj.close()
    print("table created")

except:
    print("something went wrong,table might be already exists")


win=Tk()
win.state("zoomed")
win.configure(bg="pink")
win.resizable(width=False,height=False)

title=Label(win,text="Banking Automation",font=("arial",50,"bold","underline"),bg="pink")
title.pack()

dt=time.strftime("%d %b %Y,%A")
date=Label(win,text=f"{dt}",font=("arial",20,"bold"),bg="pink",fg="blue")
date.place(relx=0.78,rely=0.1)

def main_screen():
    frm=Frame(win)
    frm.configure(bg="powder blue")
    frm.place(relx=0,rely=0.15,relheight=.85,relwidth=1)

    def forgotpass():
        frm.destroy()
        forgotpass_screen()

    def newuser():
        frm.destroy()
        newuser_screen()

    def login():
        global gacn
        gacn=e_acn.get()
        pwd=e_pass.get()
        if len(gacn)==0 or len(pwd)==0:
            messagebox.showwarning("Validation","Empty fields are not allowed")
            return
        else:
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select * from acn where acn_no=? and acn_pass=?",(gacn,pwd))
            tup=curobj.fetchone()
            conobj.close()
            if tup==None:
                messagebox.showerror("Login","Invalid Account No./Password")
            else:
                frm.destroy()
                welcome_screen()

            
    def clear():
        e_acn.delete(0,"end")
        e_pass.delete(0,"end")
        e_acn.focus()

    lbl_acn=Label(frm,text="Account  No",font=("arial",30,"bold"),bg="powder blue")
    lbl_acn.place(relx=0.15,rely=0.1)

    e_acn=Entry(frm,font=("arial",20,"bold"),bd=5)
    e_acn.place(relx=0.4,rely=0.1)
    e_acn.focus()

    lbl_pass=Label(frm,text="Password",font=("arial",30,"bold"),bg="powder blue")
    lbl_pass.place(relx=0.15,rely=0.20)

    e_pass=Entry(frm,font=("arial",20,"bold"),bd=5,show="*")
    e_pass.place(relx=0.4,rely=0.20)

    btn_login=Button(frm,text="Login",font=("arial",20,"bold"),bd=5,fg="purple",command=login)
    btn_login.place(relx=0.42,rely=0.35)

    btn_clear=Button(frm,text="Clear",font=("arial",20,"bold"),bd=5,fg="purple",command=clear)
    btn_clear.place(relx=0.55,rely=0.35)

    btn_fp=Button(frm,text="Forgot Password",font=("arial",20,"bold"),bd=5,fg="purple",width=18,command=forgotpass)
    btn_fp.place(relx=0.40,rely=0.50)

    btn_new=Button(frm,text="Open New Account",font=("arial",20,"bold"),bd=5,fg="purple",width=20,command=newuser)
    btn_new.place(relx=0.39,rely=0.66)

def forgotpass_screen():
    frm=Frame(win)
    frm.configure(bg="yellow")
    frm.place(relx=0,rely=0.15,relheight=.85,relwidth=1)
    lbl_fps=Label(frm,text="This is Forgot Password screen",font=("arial",20,"bold"),bg="yellow")
    lbl_fps.pack()
    
    def back():
        frm.destroy()
        main_screen()

    def clear1():
        e_acn.delete(0,"end")
        e_email.delete(0,"end")
        e_mob.delete(0,"end")
        e_acn.focus()

    def forgotpass_db():
        acn=e_acn.get()
        email=e_email.get()
        mob=e_mob.get()

        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select acn_pass from acn where acn_no=? and acn_email=? and acn_mob=?",(acn,email,mob))
        tup=curobj.fetchone()
        if tup==None:
            messagebox.showerror("Forgot Password","Record not found")
        else:
            messagebox.showinfo("Forgot Password",f"Your Password={tup[0]}")

        conobj.close()
        e_acn.delete(0,"end")
        e_email.delete(0,"end")
        e_mob.delete(0,"end")

        match1=re.fullmatch("[a-zA-Z0-9_]+@[a-zA-Z]+\.[a-zA-Z]+",email)
        if match1==None:
            messagebox.showwarning("Validation","Invalid format of email")
            return

        match=re.fullmatch("[6-9][0-9]{9}",mob)
        if match==None:
            messagebox.showwarning("Validation","Invalid format of mobile no entered")
            return
            

    

    btn_back=Button(frm,text="Back",font=("arial",20,"bold"),bd=5,fg="purple",command=back)
    btn_back.place(relx=0,rely=0)

    lbl_acn=Label(frm,text="Account  No",font=("arial",30,"bold"),bg="yellow")
    lbl_acn.place(relx=0.15,rely=0.1)

    e_acn=Entry(frm,font=("arial",20,"bold"),bd=5)
    e_acn.place(relx=0.4,rely=0.1)
    e_acn.focus()

    lbl_email=Label(frm,text="Email",font=("arial",30,"bold"),bg="yellow")
    lbl_email.place(relx=0.15,rely=0.25)

    e_email=Entry(frm,font=("arial",20,"bold"),bd=5)
    e_email.place(relx=0.4,rely=0.25)

    lbl_mob=Label(frm,text="Mobile No",font=("arial",30,"bold"),bg="yellow")
    lbl_mob.place(relx=0.15,rely=0.40)

    e_mob=Entry(frm,font=("arial",20,"bold"),bd=5)
    e_mob.place(relx=0.4,rely=0.40)

    btn_sub=Button(frm,text="Submit",font=("arial",20,"bold"),bd=5,fg="purple",command=forgotpass_db)
    btn_sub.place(relx=0.42,rely=0.55)

    btn_clear=Button(frm,text="Clear",font=("arial",20,"bold"),bd=5,fg="purple",command=clear1)
    btn_clear.place(relx=0.55,rely=0.55)

def newuser_screen():
    frm=Frame(win)
    frm.configure(bg="yellow")
    frm.place(relx=0,rely=0.15,relheight=.85,relwidth=1)
    lbl_oas=Label(frm,text="This is Open Account Screen",font=("arial",20,"bold"),bg="yellow")
    lbl_oas.pack()

    def back():
        frm.destroy()
        main_screen()

    def clear2():
        e_name.delete(0,"end")
        e_email.delete(0,"end")
        e_mob.delete(0,"end")
        e_pass.delete(0,"end")
        cb_gender.delete(0,"end")
        e_name.focus()

    def newuser_db():
        name=e_name.get()
        email=e_email.get()
        mob=e_mob.get()
        pwd=e_pass.get()
        gender=cb_gender.get()
        bal=0
        opendate=time.strftime("%d %b %Y,%A")

        match1=re.fullmatch("[a-zA-Z0-9_]+@[a-zA-Z]+\.[a-zA-Z]+",email)
        if match1==None:
            messagebox.showwarning("Validation","Invalid format of email")
            return


        match=re.fullmatch("[6-9][0-9]{9}",mob)
        if match==None:
            messagebox.showwarning("Validation","Invalid format of mobile no entered")
            return
    
       

        match2=re.fullmatch(r"[a-zA-Z0-9@#$%^&+=]{8}",pwd)
        if match2==None:
            messagebox.showwarning("Validation","Incorrect format of password")
            return

        
            
           
        
        

        import sqlite3
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("insert into acn(acn_name,acn_email,acn_mob,acn_pass,acn_gender,acn_opendate,acn_bal) values(?,?,?,?,?,?,?)",(name,email,mob,pwd,gender,opendate,bal))
        conobj.commit()
        conobj.close()

       
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select max(acn_no) from acn")
        tup=curobj.fetchone()
        conobj.close()
        messagebox.showinfo("New User",f"Account Created Successfully with Account No.={tup[0]}")
        e_name.delete(0,"end")
        e_email.delete(0,"end")
        e_mob.delete(0,"end")        
        e_pass.delete(0,"end")
        



    
    
    btn_back=Button(frm,text="Back",font=("arial",20,"bold"),bd=5,fg="purple",command=back)
    btn_back.place(relx=0,rely=0)

    lbl_name=Label(frm,text="Name",font=("arial",30,"bold"),bg="yellow")
    lbl_name.place(relx=0.15,rely=0.1)

    e_name=Entry(frm,font=("arial",20,"bold"),bd=5)
    e_name.place(relx=0.4,rely=0.1)
    e_name.focus()

    lbl_email=Label(frm,text="Email",font=("arial",30,"bold"),bg="yellow")
    lbl_email.place(relx=0.15,rely=0.25)

    e_email=Entry(frm,font=("arial",20,"bold"),bd=5)
    e_email.place(relx=0.4,rely=0.25)

    lbl_mob=Label(frm,text="Mobile No",font=("arial",30,"bold"),bg="yellow")
    lbl_mob.place(relx=0.15,rely=0.40)

    e_mob=Entry(frm,font=("arial",20,"bold"),bd=5)
    e_mob.place(relx=0.4,rely=0.40)

    lbl_pass=Label(frm,text="Password",font=("arial",30,"bold"),bg="yellow")
    lbl_pass.place(relx=0.15,rely=0.55)

    e_pass=Entry(frm,font=("arial",20,"bold"),bd=5,show="*")
    e_pass.place(relx=0.4,rely=0.55)

    lbl_gender=Label(frm,text="Gender",font=("arial",30,"bold"),bg="yellow")
    lbl_gender.place(relx=0.15,rely=0.70)

    cb_gender=Combobox(frm,values=["----Select----","Male","Female"],font=("arial",20,"bold"))
    cb_gender.place(relx=0.40,rely=0.70)


    btn_sub=Button(frm,text="Submit",font=("arial",20,"bold"),bd=5,fg="purple",command=newuser_db)
    btn_sub.place(relx=0.40,rely=0.80)

    btn_clear=Button(frm,text="Clear",font=("arial",20,"bold"),bd=5,fg="purple",command=clear2)
    btn_clear.place(relx=0.55,rely=0.80)

def welcome_screen():
    frm=Frame(win)
    frm.configure(bg="yellow")
    frm.place(relx=0,rely=0.15,relheight=.85,relwidth=1)

    def logout():
        frm.destroy()
        main_screen()

    def details():
        ifrm=Frame(frm,highlightbackground="black",highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=0.2,rely=0.1,relwidth=0.6,relheight=0.7)

        lbl_wel=Label(ifrm,text="This is Details Screen",font=("arial",20,"bold"),fg="blue",bg="white")
        lbl_wel.pack()

        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select acn_opendate,acn_bal,acn_gender,acn_email,acn_mob from acn where acn_no=?",(gacn,))
        tup=curobj.fetchone()
        
        
        lbl_opendate=Label(ifrm,text=f"Open Date: {tup[0]}",font=("arial",15,"bold"),bg="white")
        lbl_opendate.place(relx=0.2,rely=0.12)

        lbl_bal=Label(ifrm,text=f"Balance: {tup[1]}",font=("arial",15,"bold"),bg="white")
        lbl_bal.place(relx=0.2,rely=0.25)

        lbl_gender=Label(ifrm,text=f"Gender: {tup[2]}",font=("arial",15,"bold"),bg="white")
        lbl_gender.place(relx=0.2,rely=0.40)

        lbl_email=Label(ifrm,text=f"Email: {tup[3]}",font=("arial",15,"bold"),bg="white")
        lbl_email.place(relx=0.2,rely=0.55)

        lbl_mob=Label(ifrm,text=f"Mobile No: {tup[4]}",font=("arial",15,"bold"),bg="white")
        lbl_mob.place(relx=0.2,rely=0.70)

        conobj.close()

    def update():
        ifrm=Frame(frm,highlightbackground="black",highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=0.2,rely=0.1,relwidth=0.6,relheight=0.7)


        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select acn_name,acn_pass,acn_email,acn_mob from acn where acn_no=?",(gacn,))
        tup=curobj.fetchone()
        conobj.close()

        lbl_wel=Label(ifrm,text="This is Update Screen",font=("arial",20,"bold"),fg="blue",bg="white")
        lbl_wel.pack()

        lbl_name=Label(ifrm,text="Name",font=("arial",20,"bold"),bg="white")
        lbl_name.place(relx=0.1,rely=0.1)

        e_name=Entry(ifrm,font=("arial",20,"bold"),bd=5)
        e_name.place(relx=0.1,rely=0.20)
        e_name.insert(0,tup[0])
        e_name.focus()

        lbl_pass=Label(ifrm,text="Password",font=("arial",20,"bold"),bg="white")
        lbl_pass.place(relx=0.1,rely=0.40)

        e_pass=Entry(ifrm,font=("arial",20,"bold"),bd=5,show="*")
        e_pass.place(relx=0.1,rely=0.50)
        e_pass.insert(0,tup[1])
        
        
        lbl_email=Label(ifrm,text="Email",font=("arial",20,"bold"),bg="white")
        lbl_email.place(relx=0.55,rely=0.10)

        e_email=Entry(ifrm,font=("arial",20,"bold"),bd=5)
        e_email.place(relx=0.55,rely=0.20)
        e_email.insert(0,tup[2])
   
        lbl_mobile=Label(ifrm,text="Mobile No",font=("arial",20,"bold"),bg="white")
        lbl_mobile.place(relx=0.55,rely=0.40)

        e_mobile=Entry(ifrm,font=("arial",20,"bold"),bd=5)
        e_mobile.place(relx=0.55,rely=0.50)
        e_mobile.insert(0,tup[3])

        def update_db():
            name=e_name.get()
            pwd=e_pass.get()
            email=e_email.get()
            mob=e_mobile.get()

            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("update acn set acn_name=?,acn_pass=?,acn_email=?,acn_mob=? where acn_no=?",(name,pwd,email,mob,gacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update","Record Updated Successfully")
            welcome_screen()

        btn_update=Button(ifrm,text="Update",font=("arial",20,"bold"),bd=5,bg="blue",fg="white",command=update_db)
        btn_update.place(relx=0.80,rely=0.70)

    
    def deposit():
        ifrm=Frame(frm,highlightbackground="black",highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=0.2,rely=0.1,relwidth=0.6,relheight=0.7)

        lbl_wel=Label(ifrm,text="This is Deposit Screen",font=("arial",20,"bold"),fg="blue",bg="white")
        lbl_wel.pack()

        lbl_amt=Label(ifrm,text="Amount",font=("arial",20,"bold"),bg="white")
        lbl_amt.place(relx=0.1,rely=0.20)

        e_amt=Entry(ifrm,font=("arial",20,"bold"),bd=5)
        e_amt.place(relx=0.3,rely=0.20)
        e_amt.focus()

        def deposit_db():
            amt=float(e_amt.get())
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("update acn set acn_bal= acn_bal + ? where acn_no=?",(amt,gacn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Deposit",f"{amt} Amount Deposited")
            welcome_screen()
            

        btn_sub=Button(ifrm,text="Submit",font=("arial",20,"bold"),bd=5,bg="blue",fg="white",command=deposit_db)
        btn_sub.place(relx=0.30,rely=0.40)


    def withdraw():
        ifrm=Frame(frm,highlightbackground="black",highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=0.2,rely=0.1,relwidth=0.6,relheight=0.7)

        lbl_wel=Label(ifrm,text="This is Withdraw Screen",font=("arial",20,"bold"),fg="blue",bg="white")
        lbl_wel.pack()

        lbl_amt=Label(ifrm,text="Amount",font=("arial",20,"bold"),bg="white")
        lbl_amt.place(relx=0.1,rely=0.20)

        e_amt=Entry(ifrm,font=("arial",20,"bold"),bd=5)
        e_amt.place(relx=0.3,rely=0.20)
        e_amt.focus()

        def withdraw_db():
            amt=float(e_amt.get())
            
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select acn_bal from acn where acn_no=?",(gacn,))
            tup=curobj.fetchone()
            avail_bal=tup[0]
            conobj.close()

            if avail_bal>=amt:
                conobj=sqlite3.connect(database="bank.sqlite")
                curobj=conobj.cursor()
                curobj.execute("update acn set acn_bal= acn_bal - ? where acn_no=?",(amt,gacn))
                conobj.commit()
                conobj.close()
                messagebox.showinfo("Withdraw",f"{amt} Amount Withdrawn")
                welcome_screen()
            else:
                messagebox.showwarning("Withdraw","Insufficient Balance")
            

        btn_sub=Button(ifrm,text="Submit",font=("arial",20,"bold"),bd=5,bg="blue",fg="white",command=withdraw_db)
        btn_sub.place(relx=0.30,rely=0.40)


    def transfer():
        ifrm=Frame(frm,highlightbackground="black",highlightthickness=2)
        ifrm.configure(bg="white")
        ifrm.place(relx=0.2,rely=0.1,relwidth=0.6,relheight=0.7)

        lbl_wel=Label(ifrm,text="This is Transfer Screen",font=("arial",20,"bold"),fg="blue",bg="white")
        lbl_wel.pack()

        lbl_amt=Label(ifrm,text="Amount",font=("arial",20,"bold"),bg="white")
        lbl_amt.place(relx=0.1,rely=0.20)

        e_amt=Entry(ifrm,font=("arial",20,"bold"),bd=5)
        e_amt.place(relx=0.3,rely=0.20)
        e_amt.focus()

        lbl_to=Label(ifrm,text="To",font=("arial",20,"bold"),bg="white")
        lbl_to.place(relx=0.1,rely=0.40)

        e_to=Entry(ifrm,font=("arial",20,"bold"),bd=5)
        e_to.place(relx=0.3,rely=0.40)
        e_to.focus()

        def transfer_db():
            to_acn=e_to.get()
            amt=float(e_amt.get())

            if to_acn==gacn:
                messagebox.showwarning("Transfer","To and From can't be same")
                return
            
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select acn_bal from acn where acn_no=?",(gacn,))
            tup=curobj.fetchone()
            avail_bal=tup[0]
            conobj.close()

            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select acn_no from acn where acn_no=?",(to_acn,))
            tup=curobj.fetchone()
            conobj.close()

            if tup==None:
                messagebox.showwarning("Transfer","Invalid To Account")
                return
            
            if avail_bal>=amt:
                conobj=sqlite3.connect(database="bank.sqlite")
                curobj=conobj.cursor()
                curobj.execute("update acn set acn_bal=acn_bal+? where acn_no=?",(amt,to_acn))
                curobj.execute("update acn set acn_bal=acn_bal-? where acn_no=?",(amt,gacn))
                conobj.commit()
                conobj.close()
                messagebox.showinfo("Transfer",f"{amt} Transferred to Account {to_acn}")
                
                
                
                
            
            

        btn_sub=Button(ifrm,text="Submit",font=("arial",20,"bold"),bd=5,bg="blue",fg="white",command=transfer_db)
        btn_sub.place(relx=0.30,rely=0.60)



    conobj=sqlite3.connect(database="bank.sqlite")
    curobj=conobj.cursor()
    curobj.execute("select acn_name from acn where acn_no=?",(gacn,))
    tup=curobj.fetchone()
    conobj.close()
    
   
    
    lbl_wel=Label(frm,text=f"Welcome,{tup[0].title()}",font=("arial",20,"bold"),bg="yellow")
    lbl_wel.place(relx=0,rely=0)

    btn_logout=Button(frm,text="Logout",font=("arial",20,"bold"),bd=5,fg="purple",command=logout)
    btn_logout.place(relx=0.90,rely=0)

    btn_details=Button(frm,text="Details",font=("arial",20,"bold"),bd=5,fg="purple",width=10,command=details)
    btn_details.place(relx=0,rely=0.1)

    btn_update=Button(frm,text="Update",font=("arial",20,"bold"),bd=5,fg="purple",width=10,command=update)
    btn_update.place(relx=0,rely=0.25)

    btn_deposit=Button(frm,text="Deposit",font=("arial",20,"bold"),bd=5,fg="purple",width=10,command=deposit)
    btn_deposit.place(relx=0,rely=0.40)
    
    btn_withdraw=Button(frm,text="Withdraw",font=("arial",20,"bold"),bd=5,fg="purple",width=10,command=withdraw)
    btn_withdraw.place(relx=0,rely=0.55)

    btn_transfer=Button(frm,text="Transfer",font=("arial",20,"bold"),bd=5,fg="purple",width=10,command=transfer)
    btn_transfer.place(relx=0,rely=0.70)



main_screen()
win.title("Banking Automation by Harsh")
win.mainloop()


# In[ ]:





# # 
