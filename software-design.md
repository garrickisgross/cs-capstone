# Software Design and Engineering Enhancement

## Artifact Description

The artifact for this enhancement is my route planning web application built with FastAPI, Jinja templates, and HTMX. The original version was created early in the capstone as a basic server-side rendered application for entering and viewing delivery orders. In its initial form, the project worked, but most of the logic was tightly coupled and located in a small number of files.

## Why I Included This Artifact

I selected this artifact for the software design and engineering category because it clearly demonstrates my growth in application structure, maintainability, and separation of concerns. The original version showed that I could build a functional web app, but the enhanced version shows that I can reorganize that application into a cleaner and more scalable design.

This enhancement highlights several software development skills:

- refactoring a monolithic structure into a modular application
- separating responsibilities across routers, services, schemas, and storage layers
- using dependency injection to keep request handling clean
- improving maintainability without changing the overall purpose of the app

## Original State of the Artifact

In the original version, the FastAPI app was created directly in one main module. Static files, templates, route handlers, and order storage were all managed in the same place. Orders were stored in memory on the application object, and route handlers were responsible for both request processing and application logic. The form layer also relied on simple Python classes instead of structured validation.

This design worked for a small prototype, but it would have been difficult to maintain as the project grew.

## Enhancement Summary

The goal of this enhancement was to improve the architecture of the application without changing its overall purpose. I created a separate `software-design` branch and refactored the app into a more modular structure.

### Key Improvements

#### Application factory
I introduced a `create_app()` function to centralize app setup. This made startup behavior more organized and allowed shared dependencies to be attached cleanly during initialization.

#### Modular routing
I split route handlers into separate router modules based on feature areas. This made the code easier to navigate and kept route files focused on request handling rather than business logic.

#### Dependency management
I added a dependencies module so shared services could be injected into routes. This reduced coupling and made each endpoint clearer about what it depends on.

#### Service layer
I moved logic out of the route handlers and into service classes. This included tasks like form construction, order creation, and data formatting. That separation made the application easier to test and reason about.

#### Storage abstraction
I introduced a storage interface and an in-memory implementation rather than storing orders directly on the app. This created a clean seam for the later database enhancement.

#### Schema validation
I replaced loose Python form classes with Pydantic models. This improved structure, validation, and readability across input and stored data.

## Skills Demonstrated

This enhancement demonstrates my ability to:

- improve software architecture for maintainability
- separate concerns across application layers
- apply design patterns that fit the FastAPI framework
- prepare an application for future growth and change
- improve clarity without overcomplicating the project

## Reflection on the Enhancement Process

This enhancement taught me that good software design is often about creating clear boundaries. The original version was not broken, but it would have become harder to extend as the capstone progressed. Refactoring it forced me to think about what each part of the application was responsible for and how those parts should communicate.

One challenge was deciding how far to refactor without making the project feel overly enterprise for a capstone. I wanted the structure to be cleaner and more professional, but still appropriate for the scale of the application. Using routers, services, schemas, and a storage abstraction ended up being the right balance.

Another lesson was that architecture matters most when you need to build on top of it. This refactor directly supported the later algorithm and database enhancements. Because the application had clearer seams after this work, those later changes were easier to implement without rewriting everything.

## Course Outcome Alignment

This enhancement most strongly supports the following course outcomes:

- **Design, develop, and deliver professional-quality oral, written, and visual communications** by presenting the project in a cleaner, more understandable structure
- **Design and evaluate computing solutions that solve a given problem using computer science practices and standards** by applying layered architecture and maintainable design
- **Demonstrate an ability to use well-founded techniques, skills, and tools in computing practices** by using FastAPI patterns such as dependency injection, modular routing, and structured validation

It also partially supports the security outcome because stronger validation and cleaner data flow reduce the chance of malformed input causing problems, even though the application still does not implement full authentication or access control.
