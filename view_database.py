"""
Script to view database records directly from the command line.
Run this file with: python view_database.py
"""

from app import app, db, User, Contact, Newsletter

with app.app_context():
    print("\n" + "="*60)
    print("DATABASE RECORDS VIEWER")
    print("="*60)
    
    # View Users
    print("\n📋 REGISTERED USERS:")
    print("-" * 60)
    users = User.query.all()
    if users:
        for user in users:
            print(f"ID: {user.id} | Username: {user.username}")
            print(f"  Name: {user.first_name} {user.last_name}")
            print(f"  Email: {user.email}")
            print(f"  Created: {user.created_at}")
            print()
    else:
        print("No users registered yet.")
    
    # View Contacts
    print("\n📧 CONTACT FORM SUBMISSIONS:")
    print("-" * 60)
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    if contacts:
        for contact in contacts:
            print(f"ID: {contact.id} | From: {contact.name} ({contact.email})")
            print(f"  Subject: {contact.subject}")
            print(f"  Message: {contact.message[:100]}{'...' if len(contact.message) > 100 else ''}")
            print(f"  Date: {contact.created_at}")
            print()
    else:
        print("No contact messages yet.")
    
    # View Newsletter Subscribers
    print("\n📬 NEWSLETTER SUBSCRIBERS:")
    print("-" * 60)
    newsletters = Newsletter.query.order_by(Newsletter.subscribed_at.desc()).all()
    if newsletters:
        for newsletter in newsletters:
            print(f"ID: {newsletter.id} | Email: {newsletter.email}")
            print(f"  Subscribed: {newsletter.subscribed_at}")
            print()
    else:
        print("No newsletter subscribers yet.")
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY:")
    print(f"  Total Users: {len(users)}")
    print(f"  Total Contact Messages: {len(contacts)}")
    print(f"  Total Newsletter Subscribers: {len(newsletters)}")
    print("="*60 + "\n")
