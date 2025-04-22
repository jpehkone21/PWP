# Meetings notes

## Meeting 1.
* **DATE:** 30.1.2025
* **ASSISTANTS:** Ivan Sanchez

### Minutes
*Summary of what was discussed during the meeting*

We discussed about the API description, what we had done and what was missing. The overall idea was unique.

### Action points
*List here the actions points discussed with assistants*

- Concept diagram was not done correctly, needs fixing. TODO for next time.
- More explaining todo on the application, and why a user would want to use the app.
- Service needs explaining for next deadline.
- More info about related work.
- Justification of API missing




## Meeting 2.
* **DATE:** 18.2.2025 
* **ASSISTANTS:** Ivan Sanchez

### Minutes
*Summary of what was discussed during the meeting*

Database design and implementation were assessed. Overall it was ok, but the relation and use of foreign keys between quotes and creatures/humans/animals was incorrect. It was agreed that we fix it and send message to Ivan whether we got it to work. 

### Action points
*List here the actions points discussed with assistants*
- Instructions for installing requirements was missing
- Diagram about the database models needs changes (arrows should be the other way around, need to add text if relations are one-one, many-one etc.)
- The relation between quotes and creature/humans/animals was done incorrectly. Foreign key should be only in creatures/humans/animals and not in quotes.
- (Suggestion that the name attribute could be the primary key for creatures/humans/animals)
- (Suggestion that creature types could be constrained in db or in api) 

## Meeting 3.
* **DATE:** 25.3.2025
* **ASSISTANTS:** Ivan Sanchez

### Minutes
*Summary of what was discussed during the meeting*

We discussed the API implementation and the tests related to it. 

### Action points
*List here the actions points discussed with assistants*

The API worked and passed the tests we had prepared. However, some issues and possible improvements were discovered in the meeting:
- Schema validation was not done in POST methods
- Not Found error returns html
- Wrong error code for PUT if body is empty
- Test coverage needs to be added for humans and animals (add same tests that were done to creature)
- Add examples about uniform interface to wiki



## Meeting 4.
* **DATE:** 15.4.2025
* **ASSISTANTS:** Ivan Sanchez

### Minutes
*Summary of what was discussed during the meeting*

Documentation was assessed (We decided not to implemented hypermedia). At the end we discussed our plans for a client and possibly using chatgpt for an additional service.

### Action points
*List here the actions points discussed with assistants*

Documentation overall was good, but it had some small things that need to be fixed:
- Parameters were not global
- Error response examples were missing the body
- Not found response was missing in some routes that had name parameter



## Midterm meeting
* **DATE:**
* **ASSISTANTS:**

### Minutes
*Summary of what was discussed during the meeting*

### Action points
*List here the actions points discussed with assistants*




## Final meeting
* **DATE:**
* **ASSISTANTS:**

### Minutes
*Summary of what was discussed during the meeting*

### Action points
*List here the actions points discussed with assistants*




