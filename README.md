# Linguistic Atlas API  
*A data-driven system for exploring global language relationships*

This project was developed for **COMP3011 Web Services and Web Data** at the **University of Leeds**.

The *Linguistic Atlas API* transforms the **Glottolog linguistic dataset** into a structured, queryable web service, enabling users to explore how languages relate to one another across both **historical classification hierarchies** and **geographical distribution**.

Rather than acting as a simple data wrapper, the system focuses on exposing **relationships**, allowing languages to be analysed as part of larger families, macroareas, and evolutionary structures.

---

## Motivation

Linguistic data is often:

- difficult to navigate programmatically  
- distributed across static datasets  
- lacking accessible relational structure  

This API addresses these limitations by:

- structuring language data into a **navigable hierarchy**
- enabling **programmatic exploration of linguistic relationships**
- supporting **visualisation through map-based interfaces**

---

## ⚙️ System Overview

The API is designed around three key capabilities:

### Hierarchical Exploration
- Traverse language → family relationships
- Reconstruct full classification trees dynamically
- Support recursive parent-child traversal

### Data Access & Filtering
- Retrieve languages and metadata
- Search by name
- Filter by macroarea, country, and level
- Pagination for scalable queries

### Analytical Insights
- Aggregate languages by macroarea and family
- Identify distribution patterns
- Enable higher-level linguistic analysis

---

## Visualisation Capability

The API supports **map-based visualisation**, enabling:

- plotting of languages using geographic coordinates  
- grouping by macroarea  
- identification of regional linguistic density  

This transforms the API from a data source into an **interactive exploration tool**.

---

## Security

All endpoints are protected using **API key authentication** via request headers.

Example:
```http
X-API-Key: secret123