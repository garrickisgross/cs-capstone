# Database Enhancement

## Artifact Description

The artifact for this enhancement is my capstone route planning web application built with FastAPI, Jinja templates, and HTMX. The original version stored all order data in memory, which meant the application lost that information whenever it restarted. In this enhancement, I added a SQLite persistence layer so that orders could be stored and reused across sessions.

## Why I Included This Artifact

I selected this artifact because it demonstrates practical database integration within an existing application. Instead of building a disconnected database example, I enhanced a working project in a way that improved its real functionality.

This enhancement highlights several database-related skills:

- designing a relational table to support application workflows
- integrating SQLite into an existing architecture
- performing insert, query, and update operations
- preserving application structure by using a shared storage abstraction

## Enhancement Summary

The main goal of this enhancement was to replace temporary in-memory storage with persistent storage while keeping the rest of the application as stable as possible.

### Key Improvements

#### SQLite storage layer
I implemented a new `SQLiteStorage` class to manage persistence. This class created and interacted with an `orders` table that stores order information, address fields, coordinates, and an optimized flag.

#### Persistent data across sessions
Unlike the original in-memory approach, SQLite allows orders to remain available after the application restarts. This made the artifact more realistic and more useful.

#### CRUD-style operations
I implemented the core operations needed by the application, including inserting orders, reading stored orders, filtering unoptimized orders, and marking orders as optimized after route generation.

#### Reuse of the storage interface
Because I had already introduced a storage abstraction during the software design enhancement, I was able to add SQLite without rewriting the rest of the app. The new persistence layer could be swapped in cleanly.

#### Testing
I added tests to verify that persisted orders could be inserted, retrieved, filtered, and updated correctly. This gave me more confidence that the database behavior supported the application workflow.

## Skills Demonstrated

This enhancement demonstrates my ability to:

- design a schema that matches application needs
- integrate a relational database into a Python web application
- implement application-driven data operations
- preserve separation of concerns between storage and business logic
- validate persistence behavior with testing

## Reflection on the Enhancement Process

This enhancement helped me better understand how persistence changes application design. Moving from in-memory data to SQLite required me to think differently about how information is stored, retrieved, and maintained over time.

The biggest lesson I learned was the value of abstraction. Because the application already had a storage interface, I did not have to rebuild the entire project to add the database. That made the change much cleaner and reinforced the importance of planning for future extension.

One challenge was making sure the database structure supported the workflow already established in the app. I needed the schema to store both address information and the geographic data used by the optimization logic. I also needed to keep the implementation simple enough to fit the capstone while still demonstrating meaningful database work.

## Course Outcome Alignment

This enhancement strongly supports the following course outcomes:

- **Demonstrate an ability to use well-founded techniques, skills, and tools in computing practices** by integrating SQLite into an existing application in a practical way
- **Design and evaluate computing solutions that solve a given problem using computer science practices and standards** by creating a persistence layer that supports the project workflow
- **Develop professional-quality communications** by clearly explaining how the database enhancement improved the artifact

It also partially supports the security outcome because the SQLite layer uses parameterized operations and a more structured data flow, even though the application still does not implement broader production-level security controls.
