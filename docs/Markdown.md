# Linguistic Atlas API Documentation

All URIs are relative to `https://web-production-88604.up.railway.app`

## Documentation for API Endpoints

| Group | Method | HTTP Request | Description |
|-------|--------|-------------|-------------|
| *CoreApi* | [**root**](#root) | **GET** / | Root |
| *CoreApi* | [**health**](#health) | **GET** /health | Health |
| *AuthApi* | [**register**](#register) | **POST** /auth/register | Register |
| *AuthApi* | [**login**](#login) | **POST** /auth/login | Login |
| *AuthApi* | [**me**](#me) | **GET** /auth/me | Me |
| *LanguagesApi* | [**getLanguages**](#getLanguages) | **GET** /languages | Explore the world's languages |
| *LanguagesApi* | [**getLanguagesMap**](#getLanguagesMap) | **GET** /languages/map | Visualise languages geographically |
| *LanguagesApi* | [**searchLanguages**](#searchLanguages) | **GET** /languages/search | Search languages by name |
| *LanguagesApi* | [**getRandomLanguage**](#getRandomLanguage) | **GET** /languages/random | Discover a random language |
| *LanguagesApi* | [**getLanguageByIso**](#getLanguageByIso) | **GET** /languages/iso/{iso_code} | Look up a language by ISO 639-3 code |
| *LanguagesApi* | [**getLanguage**](#getLanguage) | **GET** /languages/{language_id} | Get a language by Glottolog ID |
| *LanguagesApi* | [**getLanguageNames**](#getLanguageNames) | **GET** /languages/{language_id}/names | List all known names for a language |
| *LanguagesApi* | [**getLanguageClassification**](#getLanguageClassification) | **GET** /languages/{language_id}/classification | Trace the genealogical family tree |
| *LanguagesApi* | [**getLanguageParameters**](#getLanguageParameters) | **GET** /languages/{language_id}/parameters | Get typological features |
| *LanguagesApi* | [**getLanguageEndangerment**](#getLanguageEndangerment) | **GET** /languages/{language_id}/endangerment | How at risk is this language? |
| *FamiliesApi* | [**getFamilies**](#getFamilies) | **GET** /families | Browse language families |
| *FamiliesApi* | [**getFamily**](#getFamily) | **GET** /families/{family_id} | Get a family by Glottolog ID |
| *FamiliesApi* | [**getFamilyLanguages**](#getFamilyLanguages) | **GET** /families/{family_id}/languages | List languages within a family |
| *MacroareasApi* | [**getMacroareas**](#getMacroareas) | **GET** /macroareas | List all geographic macroareas |
| *MacroareasApi* | [**getMacroareaLanguages**](#getMacroareaLanguages) | **GET** /macroareas/{macroarea}/languages | Browse languages by macroarea |
| *StatsApi* | [**languagesPerMacroarea**](#languagesPerMacroarea) | **GET** /stats/languages-per-macroarea | Language distribution by macroarea |
| *StatsApi* | [**languagesPerFamily**](#languagesPerFamily) | **GET** /stats/languages-per-family | Top 50 families by language count |
| *StatsApi* | [**endangermentBreakdown**](#endangermentBreakdown) | **GET** /stats/endangerment-breakdown | How many of the world's languages are at risk? |
| *StatsApi* | [**underdocumented**](#underdocumented) | **GET** /stats/underdocumented | Languages going silent: at risk and unstudied for decades |
| *TestimoniesApi* | [**listTestimonies**](#listTestimonies) | **GET** /language-sets | Every Testimony ever recorded |
| *TestimoniesApi* | [**createTestimony**](#createTestimony) | **POST** /language-sets | Bear witness — begin a new Testimony |
| *TestimoniesApi* | [**getTestimony**](#getTestimony) | **GET** /language-sets/{set_id} | Open a Testimony and read its intent |
| *TestimoniesApi* | [**updateTestimony**](#updateTestimony) | **PATCH** /language-sets/{set_id} | Revise the record — update a Testimony |
| *TestimoniesApi* | [**deleteTestimony**](#deleteTestimony) | **DELETE** /language-sets/{set_id} | Silence a Testimony — erase it permanently |
| *TestimoniesApi* | [**addLanguage**](#addLanguage) | **POST** /language-sets/{set_id}/languages | Add a voice to the record |
| *TestimoniesApi* | [**listLanguages**](#listLanguages) | **GET** /language-sets/{set_id}/languages | The voices — every language in collection |
| *TestimoniesApi* | [**removeLanguage**](#removeLanguage) | **DELETE** /language-sets/{set_id}/languages/{item_id} | Remove a voice from this Testimony |
| *TestimoniesApi* | [**getInsights**](#getInsights) | **GET** /language-sets/{set_id}/insights | What will be lost — the full portrait of a Testimony |
| *AnalyticsApi* | [**similarity**](#similarity) | **GET** /analytics/similarity | How closely related are two languages? |
| *AnalyticsApi* | [**compareSets**](#compareSets) | **POST** /analytics/compare-sets | Where do two Testimonies overlap? |
| *AnalyticsApi* | [**outliers**](#outliers) | **GET** /analytics/outliers | Languages that slipped through the cracks |
| *AnalyticsApi* | [**lineage**](#lineage) | **GET** /analytics/lineage/{language_id} | Trace a language back to its oldest known ancestor |
| *AnalyticsApi* | [**coverage**](#coverage) | **GET** /analytics/coverage/{language_id} | How well documented is this language? |
| *AnalyticsApi* | [**setProfile**](#setProfile) | **GET** /analytics/language-sets/{set_id}/profile | The DNA of a Testimony — families, regions, diversity |
| *AskApi* | [**ask**](#ask) | **POST** /ask | Ask the Atlas anything |

---

## Documentation for Authorization

### API Key
All endpoints require an `X-API-Key` header.

```
X-API-Key: your_api_key
```

### Bearer Token (JWT)
Write operations on language sets require a JWT bearer token obtained from `/auth/login`.

```
Authorization: Bearer <token>
```

---

## Core

<a name="root"></a>
### **root**
**GET** /

Returns a message confirming the API is running.

#### Return type
```json
{ "message": "Linguistic Atlas API is running" }
```

#### Authorization
API Key required.

#### HTTP request headers
- **Accept**: application/json

---

<a name="health"></a>
### **health**
**GET** /health

Returns the health status of the API.

#### Return type
```json
{ "status": "ok" }
```

#### Authorization
API Key required.

---

## Auth

<a name="register"></a>
### **register**
**POST** /auth/register

Register a new user account.

#### Request body
```json
{
  "email": "researcher@linguisticatlas.com",
  "password": "yourpassword123"
}
```

#### Return type
```json
{ "message": "User created" }
```

#### Authorization
API Key required.

#### HTTP request headers
- **Content-Type**: application/json
- **Accept**: application/json

---

<a name="login"></a>
### **login**
**POST** /auth/login

Login and receive a JWT access token.

#### Request body
```json
{
  "email": "researcher@linguisticatlas.com",
  "password": "yourpassword123"
}
```

#### Return type
```json
{ "access_token": "eyJ..." }
```

#### Authorization
API Key required.

#### HTTP request headers
- **Content-Type**: application/json
- **Accept**: application/json

---

<a name="me"></a>
### **me**
**GET** /auth/me

Returns the decoded JWT payload for the current user.

#### Parameters
| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **token** | **String** | JWT access token | Required |

#### Authorization
API Key required.

---

## Languages

<a name="getLanguages"></a>
### **getLanguages**
**GET** /languages

Returns a paginated list of languages with optional filters.

#### Parameters
| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **limit** | **Integer** | Number of results to return | [optional] [default: 20] [max: 500] |
| **offset** | **Integer** | Number of results to skip | [optional] [default: 0] |
| **macroarea** | **String** | Filter by macroarea (e.g. Africa, Eurasia) | [optional] |
| **level** | **String** | Filter by level (language, dialect, family) | [optional] |
| **country** | **String** | Filter by country name or ISO code | [optional] |

#### Return type
Array of Language objects, each including `endangerment` and `at_risk` fields.

#### Example response
```json
[
  {
    "id": "stan1295",
    "name": "Somali",
    "macroarea": "Africa",
    "latitude": 6.0,
    "longitude": 46.0,
    "iso_code": "som",
    "level": "language",
    "family_id": "afro1255",
    "endangerment": "Not Endangered",
    "at_risk": false
  }
]
```

#### Authorization
API Key required.

---

<a name="getLanguagesMap"></a>
### **getLanguagesMap**
**GET** /languages/map

Returns a lightweight list of languages with geographic coordinates for map visualisation.

#### Parameters
| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **limit** | **Integer** | Number of results | [optional] [default: 500] [max: 2000] |

#### Example response
```json
[
  {
    "ID": "stan1295",
    "Name": "Somali",
    "Macroarea": "Africa",
    "Latitude": 6.0,
    "Longitude": 46.0,
    "Level": "language",
    "ISO639P3code": "som"
  }
]
```

#### Authorization
API Key required.

---

<a name="searchLanguages"></a>
### **searchLanguages**
**GET** /languages/search

Case-insensitive substring search on language names. Returns results with inline endangerment status.

#### Parameters
| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **name** | **String** | Partial or full language name | Required |
| **limit** | **Integer** | Number of results | [optional] [default: 20] [max: 100] |
| **offset** | **Integer** | Pagination offset | [optional] [default: 0] |

#### Authorization
API Key required.

---

<a name="getRandomLanguage"></a>
### **getRandomLanguage**
**GET** /languages/random

Returns a single randomly selected language with endangerment status included.

#### Authorization
API Key required.

---

<a name="getLanguageByIso"></a>
### **getLanguageByIso**
**GET** /languages/iso/{iso_code}

Look up a language by its ISO 639-3 three-letter code (case-insensitive).

#### Parameters
| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **iso_code** | **String** | ISO 639-3 code (e.g. som, eng, zho) | Required |

#### Authorization
API Key required.

---

<a name="getLanguage"></a>
### **getLanguage**
**GET** /languages/{language_id}

Returns full details for a language by its Glottolog ID.

#### Parameters
| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **language_id** | **String** | Glottolog ID (e.g. stan1295) | Required |

#### Authorization
API Key required.

---

<a name="getLanguageNames"></a>
### **getLanguageNames**
**GET** /languages/{language_id}/names

Returns all known names and alternative spellings for a language across sources.

#### Parameters
| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **language_id** | **String** | Glottolog ID | Required |

#### Example response
```json
[
  {
    "id": 1,
    "source_id": "glottolog",
    "language_id": "stan1295",
    "name": "Af Soomaali",
    "provider": "Ethnologue",
    "lang": "som"
  }
]
```

#### Authorization
API Key required.

---

<a name="getLanguageClassification"></a>
### **getLanguageClassification**
**GET** /languages/{language_id}/classification

Traverses the Glottolog family tree upward and returns the full genealogical classification from top-level family to the language itself.

#### Parameters
| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **language_id** | **String** | Glottolog ID | Required |

#### Example response
```json
{
  "language_id": "stan1295",
  "language_name": "Somali",
  "classification": [
    { "id": "afro1255", "name": "Afro-Asiatic", "level": "family" },
    { "id": "cush1243", "name": "Cushitic", "level": "family" },
    { "id": "east2699", "name": "East Cushitic", "level": "family" },
    { "id": "stan1295", "name": "Somali", "level": "language" }
  ]
}
```

#### Authorization
API Key required.

---

<a name="getLanguageParameters"></a>
### **getLanguageParameters**
**GET** /languages/{language_id}/parameters

Returns all WALS and Glottolog typological parameter values for a language.

#### Parameters
| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **language_id** | **String** | Glottolog ID | Required |

#### Example response
```json
[
  {
    "parameter_id": "aes",
    "parameter_name": "Agglomerated Endangerment Status",
    "value": "1",
    "code_id": "aes-not_endangered",
    "code_name": "not endangered",
    "code_description": "EGIDS: <=6a; UNESCO: safe; ElCat: safe",
    "comment": null,
    "source": "Glottolog"
  }
]
```

#### Authorization
API Key required.

---

<a name="getLanguageEndangerment"></a>
### **getLanguageEndangerment**
**GET** /languages/{language_id}/endangerment

Returns a plain-English endangerment profile based on Glottolog AES data, including risk summary, years since last documentation, and documentation status label.

#### Parameters
| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **language_id** | **String** | Glottolog ID | Required |

#### Example response
```json
{
  "language_id": "bura1267",
  "name": "Burak",
  "aes_code": "aes-moribund",
  "status": "Moribund",
  "at_risk": true,
  "severity": 4,
  "what_this_means": "EGIDS: 8a; UNESCO: severely endangered",
  "first_documented": 1932,
  "last_documented": 1987,
  "years_documented": 55,
  "years_since_last_study": 38,
  "documentation_status": "Decades since last study",
  "is_isolate": false,
  "macroarea": "Africa",
  "risk_summary": "Moribund — only a few elderly speakers remain. Unlikely to survive another generation without active revitalisation."
}
```

#### Authorization
API Key required.

---

## Families

<a name="getFamilies"></a>
### **getFamilies**
**GET** /families

Returns a paginated list of language families.

#### Parameters
| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **limit** | **Integer** | Number of results | [optional] [default: 20] [max: 100] |
| **offset** | **Integer** | Pagination offset | [optional] [default: 0] |

#### Authorization
API Key required.

---

<a name="getFamily"></a>
### **getFamily**
**GET** /families/{family_id}

Returns a single language family by Glottolog ID.

#### Parameters
| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **family_id** | **String** | Glottolog ID of the family | Required |

#### Authorization
API Key required.

---

<a name="getFamilyLanguages"></a>
### **getFamilyLanguages**
**GET** /families/{family_id}/languages

Returns all languages that directly belong to the given family.

#### Parameters
| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **family_id** | **String** | Glottolog ID of the family | Required |
| **limit** | **Integer** | Number of results | [optional] [default: 20] [max: 100] |
| **offset** | **Integer** | Pagination offset | [optional] [default: 0] |

#### Authorization
API Key required.

---

## Macroareas

<a name="getMacroareas"></a>
### **getMacroareas**
**GET** /macroareas

Returns a deduplicated sorted list of all macroarea names in the dataset.

#### Example response
```json
[
  { "macroarea": "Africa" },
  { "macroarea": "Australia" },
  { "macroarea": "Eurasia" },
  { "macroarea": "North America" },
  { "macroarea": "Papunesia" },
  { "macroarea": "South America" }
]
```

#### Authorization
API Key required.

---

<a name="getMacroareaLanguages"></a>
### **getMacroareaLanguages**
**GET** /macroareas/{macroarea}/languages

Returns languages associated with the given macroarea.

#### Parameters
| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **macroarea** | **String** | Macroarea name (e.g. Africa) | Required |
| **limit** | **Integer** | Number of results | [optional] [default: 20] [max: 100] |
| **offset** | **Integer** | Pagination offset | [optional] [default: 0] |

#### Authorization
API Key required.

---

## Stats

<a name="languagesPerMacroarea"></a>
### **languagesPerMacroarea**
**GET** /stats/languages-per-macroarea

Returns a dictionary mapping each macroarea to its language count, sorted descending.

#### Example response
```json
{
  "Africa": 2148,
  "Papunesia": 1984,
  "South America": 1058,
  "North America": 912,
  "Eurasia": 890,
  "Australia": 387
}
```

#### Authorization
API Key required.

---

<a name="languagesPerFamily"></a>
### **languagesPerFamily**
**GET** /stats/languages-per-family

Returns the top 50 language families by member count.

#### Example response
```json
{
  "Niger-Congo": 1540,
  "Austronesian": 1248,
  "Indo-European": 437
}
```

#### Authorization
API Key required.

---

<a name="endangermentBreakdown"></a>
### **endangermentBreakdown**
**GET** /stats/endangerment-breakdown

Returns counts of all languages grouped by AES endangerment level, compiled from UNESCO, EGIDS, and ElCat sources.

#### Example response
```json
{
  "total_with_aes_data": 6842,
  "breakdown": {
    "Not Endangered": 3201,
    "Threatened": 964,
    "Shifting": 748,
    "Moribund": 591,
    "Nearly Extinct": 412,
    "Extinct": 926
  },
  "at_risk_total": 2715,
  "source": "Glottolog AES — compiled from UNESCO, EGIDS, and ElCat"
}
```

#### Authorization
API Key required.

---

<a name="underdocumented"></a>
### **underdocumented**
**GET** /stats/underdocumented

Returns endangered languages that have not been studied since before a given year, sorted by oldest first.

#### Parameters
| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **before** | **Integer** | Only include languages last documented before this year | [optional] [default: 1970] |

#### Example response
```json
{
  "count": 3,
  "threshold_year": 1970,
  "languages": [
    {
      "language_id": "xyz1234",
      "name": "Taurap",
      "macroarea": "Papunesia",
      "last_documented": 1953,
      "years_of_silence": 72,
      "endangerment": "Nearly Extinct"
    }
  ]
}
```

#### Authorization
API Key required.

---

## Testimonies (Language Sets)

<a name="listTestimonies"></a>
### **listTestimonies**
**GET** /language-sets

Returns all saved Testimonies.

#### Authorization
API Key required.

---

<a name="createTestimony"></a>
### **createTestimony**
**POST** /language-sets

Creates a new Testimony. Requires a valid JWT.

#### Request body
```json
{
  "title": "Voices on the Edge",
  "description": "Languages classified as moribund or nearly extinct across Sub-Saharan Africa",
  "notes": "Focus on languages with fewer than 100 remaining speakers"
}
```

#### Authorization
API Key + JWT Bearer Token required.

#### HTTP request headers
- **Content-Type**: application/json
- **Accept**: application/json

---

<a name="getTestimony"></a>
### **getTestimony**
**GET** /language-sets/{set_id}

Returns a single Testimony by ID.

#### Parameters
| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **set_id** | **Integer** | Testimony ID | Required |

#### Authorization
API Key required.

---

<a name="updateTestimony"></a>
### **updateTestimony**
**PATCH** /language-sets/{set_id}

Updates a Testimony. All fields are optional.

#### Parameters
| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **set_id** | **Integer** | Testimony ID | Required |

#### Request body
```json
{
  "title": "Voices on the Edge — Revised",
  "description": "Expanded to include languages from the Horn of Africa"
}
```

#### Authorization
API Key required.

---

<a name="deleteTestimony"></a>
### **deleteTestimony**
**DELETE** /language-sets/{set_id}

Permanently deletes a Testimony and all its languages. Admin only.

#### Parameters
| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **set_id** | **Integer** | Testimony ID | Required |

#### Authorization
API Key + JWT Bearer Token (Admin role) required.

---

<a name="addLanguage"></a>
### **addLanguage**
**POST** /language-sets/{set_id}/languages

Adds a language to a Testimony by Glottolog ID.

#### Parameters
| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **set_id** | **Integer** | Testimony ID | Required |

#### Request body
```json
{
  "language_id": "soma1255"
}
```

#### Authorization
API Key required.

---

<a name="listLanguages"></a>
### **listLanguages**
**GET** /language-sets/{set_id}/languages

Returns all languages in a Testimony with endangerment status and recorded name count.

#### Parameters
| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **set_id** | **Integer** | Testimony ID | Required |

#### Authorization
API Key required.

---

<a name="removeLanguage"></a>
### **removeLanguage**
**DELETE** /language-sets/{set_id}/languages/{item_id}

Removes a single language from a Testimony by item ID.

#### Parameters
| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **set_id** | **Integer** | Testimony ID | Required |
| **item_id** | **Integer** | Item ID | Required |

#### Authorization
API Key required.

---

<a name="getInsights"></a>
### **getInsights**
**GET** /language-sets/{set_id}/insights

Runs a full analysis across every language in the Testimony. Returns endangerment breakdown, family diversity, geographic spread, languages likely extinct before 2100, language isolates, and the least documented language in the set.

#### Parameters
| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **set_id** | **Integer** | Testimony ID | Required |

#### Example response
```json
{
  "testimony": "Voices on the Edge",
  "language_count": 10,
  "endangerment_breakdown": {
    "Moribund": 4,
    "Nearly Extinct": 3,
    "Extinct": 2,
    "Unknown": 1
  },
  "at_risk_count": 9,
  "likely_extinct_before_2100": {
    "count": 7,
    "languages": [
      {
        "language_id": "xyz1234",
        "name": "Taurap",
        "status": "Nearly Extinct",
        "macroarea": "Papunesia"
      }
    ],
    "note": "Classified as moribund, nearly extinct, or already extinct per Glottolog AES data."
  },
  "families_represented": {
    "count": 5,
    "breakdown": { "Afro-Asiatic": 4, "Niger-Congo": 3 }
  },
  "geographic_spread": {
    "macroareas_covered": 3,
    "breakdown": { "Africa": 6, "Eurasia": 3, "Papunesia": 1 }
  },
  "language_isolates": {
    "count": 1,
    "languages": [{ "id": "basq1248", "name": "Basque", "macroarea": "Eurasia" }],
    "note": "Isolates have no known relatives — if lost, their entire branch of human language disappears."
  },
  "most_undocumented": {
    "language_id": "xyz1234",
    "name": "Taurap",
    "recorded_names": 1,
    "note": "The language in this Testimony recorded under the fewest distinct names across all sources."
  }
}
```

#### Authorization
API Key required.

---

## Analytics

<a name="similarity"></a>
### **similarity**
**GET** /analytics/similarity

Computes a normalised 0–1 similarity score between two languages based on shared family classification, macroarea proximity, and isolate status.

#### Parameters
| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **lang1** | **String** | Glottolog ID of first language | Required |
| **lang2** | **String** | Glottolog ID of second language | Required |

#### Example response
```json
{
  "language1": "Somali",
  "language2": "Oromo",
  "similarity_score": 0.8,
  "insight": "Closely related languages",
  "explanation": ["Same language family", "Same macroarea"]
}
```

#### Authorization
API Key required.

---

<a name="compareSets"></a>
### **compareSets**
**POST** /analytics/compare-sets

Measures overlap between two Testimonies, returning shared and unique language counts and an overlap ratio.

#### Parameters
| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **set1_id** | **Integer** | First Testimony ID | Required |
| **set2_id** | **Integer** | Second Testimony ID | Required |

#### Example response
```json
{
  "shared_count": 4,
  "unique_set1": 6,
  "unique_set2": 3,
  "overlap_ratio": 0.4
}
```

#### Authorization
API Key required.

---

<a name="outliers"></a>
### **outliers**
**GET** /analytics/outliers

Identifies languages that stand out due to missing family classification, isolate status, or very low parameter coverage.

#### Example response
```json
{
  "count": 2,
  "outliers": [
    {
      "language_id": "basq1248",
      "name": "Basque",
      "coverage": 3,
      "is_isolate": true,
      "reasons": ["Language isolate", "Very low parameter coverage"]
    }
  ]
}
```

#### Authorization
API Key required.

---

<a name="lineage"></a>
### **lineage**
**GET** /analytics/lineage/{language_id}

Traverses the classification tree upward from a language to its oldest known ancestor.

#### Parameters
| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **language_id** | **String** | Glottolog ID | Required |

#### Example response
```json
{
  "language_id": "stan1295",
  "lineage": [
    { "id": "afro1255", "name": "Afro-Asiatic" },
    { "id": "cush1243", "name": "Cushitic" },
    { "id": "east2699", "name": "East Cushitic" },
    { "id": "stan1295", "name": "Somali" }
  ]
}
```

#### Authorization
API Key required.

---

<a name="coverage"></a>
### **coverage**
**GET** /analytics/coverage/{language_id}

Measures how well documented a language is by comparing its recorded parameter count against the full parameter set.

#### Parameters
| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **language_id** | **String** | Glottolog ID | Required |

#### Example response
```json
{
  "language_id": "stan1295",
  "parameter_count": 42,
  "total_parameters": 200,
  "coverage_score": 0.21
}
```

#### Authorization
API Key required.

---

<a name="setProfile"></a>
### **setProfile**
**GET** /analytics/language-sets/{set_id}/profile

Generates a breakdown of a Testimony including family distribution, macroarea coverage, and a diversity score.

#### Parameters
| Name | Type | Description | Notes |
|------|------|-------------|-------|
| **set_id** | **Integer** | Testimony ID | Required |

#### Example response
```json
{
  "set_id": 1,
  "total_languages": 10,
  "family_distribution": { "afro1255": 4, "indo1319": 3, "Unknown": 3 },
  "macroarea_distribution": { "Africa": 5, "Eurasia": 3, "North America": 2 },
  "diversity_score": 0.3
}
```

#### Authorization
API Key required.

---

## Ask the Atlas

<a name="ask"></a>
### **ask**
**POST** /ask

Submit a natural language question about the linguistic dataset. The AI routes the query to the appropriate analytical endpoints automatically using the Anthropic API.

#### Request body
```json
{
  "question": "How similar are Somali and Oromo? Are they from the same family?"
}
```

#### Return type
```json
{
  "answer": "Somali and Oromo are both Cushitic languages within the Afro-Asiatic family..."
}
```

#### Authorization
API Key required.

#### HTTP request headers
- **Content-Type**: application/json
- **Accept**: application/json

---

## Error Codes

| Status Code | Meaning |
|-------------|---------|
| 200 | Successful read |
| 201 | Resource created |
| 400 | Bad request (e.g. duplicate language in Testimony) |
| 401 | Missing or invalid API key |
| 403 | Insufficient role (admin required) |
| 404 | Resource not found |
| 422 | Validation error — response body identifies which field failed |