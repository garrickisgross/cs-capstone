# Artifact Overview

The artifact used throughout this ePortfolio is a route planning web application developed as part of my Computer Science capstone. The project is a server-side rendered web application built with FastAPI, Jinja templates, and HTMX. It allows users to create delivery orders, view stored orders, and generate optimized routes based on geographic data.

I selected this artifact because it gave me the best opportunity to demonstrate growth across all three required enhancement categories using one continuous project. Instead of presenting unrelated assignments, I was able to show how one application evolved over time through architectural refactoring, algorithmic improvement, and database integration.

## Why This Artifact Works Well for the Portfolio

This project represents more than a simple classroom exercise. It reflects how multiple areas of computer science work together in a practical application:

- software design and engineering through modular architecture and improved maintainability
- algorithms and data structures through geographic calculations, distance matrices, and route optimization
- databases through persistent SQLite storage and structured data access

Using one artifact across all three categories also made the portfolio more cohesive. Each enhancement builds on the previous one. The software design refactor created clearer boundaries in the application. Those boundaries made it easier to add route optimization logic and later replace in-memory storage with a SQLite database.

## Original State of the Project

The original version of the application was functional but simple. The FastAPI app, templates, routes, and in-memory data handling were all closely tied together. Orders were stored in memory, so restarting the application cleared all data. Route optimization had not yet been fully implemented, and the code structure was not designed for easy scaling or long-term maintenance.

## Enhancement Path

The enhanced artifact developed in three major stages:

1. **Software Design and Engineering**  
   I refactored the application into a more maintainable structure using routers, services, schemas, dependency injection, and a storage abstraction.

2. **Algorithms and Data Structures**  
   I added geographic logic using the Haversine formula, built a distance matrix, and implemented a 2-opt optimization algorithm to improve route ordering.

3. **Databases**  
   I introduced persistent storage with SQLite, allowing orders to remain available across application restarts without redesigning the rest of the app.

## What the Pages That Follow Show

Each enhancement page explains:

- what the artifact is and when it was created
- why I selected it for the ePortfolio
- what specific improvements were made
- what skills were demonstrated
- what I learned during the enhancement process
- which course outcomes were met fully or partially

Together, these pages show both technical development and reflection, which is the core purpose of the capstone ePortfolio.
