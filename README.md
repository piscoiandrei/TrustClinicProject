Web Application for a chain of clinics with AsyncChat for customer service, Appointment Management System for clients/pacients and doctors and some other features.

Main Design:

The application is split into 5 main perspectives, each with it's own unique functions:
 1.Guest Perspective
 2.Client Perspective
 3.Operator Perspective
 4.Doctor Perspective
 5.Admin Perspective
Each user is redirected on login according to their roles.

Main features for each perspective:
  1. The guest has access only to the first page, and the authentication pages, the web app is meant to be used with an account.
  2. The client can browse the clinics,specializations and doctors to make an appointment. The client can edit its own profile. There is also a live chat feature where the client can chat with an operator.
  3. The operator can have multiple chats open at once, and can switch between them, it can also close them.
  4. The doctor can see all its appointments in chronological order and it can delete them. The doctor can modify his profile and the working hours for every day in the week.
  5. The admin perspective is the default one from Django, but a bit customized and improved.
