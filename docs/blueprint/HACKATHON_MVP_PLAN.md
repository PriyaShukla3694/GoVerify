# MVP Plan & Intentional Corners Cut

In a 48-hour competitive format, chasing perfection inevitably tanks the demo. We actively bypass specific technical hurdles for the MVP mapping:

## Trade-off 1: Synthetic Over Real Data
The AI mechanism depends critically on ML boundaries simulating actual struggle thresholds. Gathering real typing sets is impossible. **Solution**: We procedurally generate random values bounding statistics (slow users: 5-15 WPM, huge pause delays) mapping directly as our data sets in `scikit-learn`.

## Trade-off 2: SQLite Extrapolations
Normally, scaling this across an entire state warrants heavy Postgres setups and Docker layers. To avoid 5 hour debug sessions locally, **Solution**: We inject a zero-ops `.sqlite` native file operating linearly entirely handling presentation loads securely up to 50 concurrent transactions. 

## Trade-off 3: Location Datasets Limit
The scale of mapping exact Revenue Villages dynamically per Indian region is staggering. **Solution**: The Smart Autofill logic uses a hardcoded SQLite dictionary explicitly modeling roughly an isolated geography boundary (for example, Uttarakhand 5 specific tehsils mapping 50 localized demo villages).

## Trade-off 4: Authentication Abstraction
Adding Auth0 and JWT login schemas absorbs extreme bandwidth while confusing the narrative. **Solution**: For the MVP presentation, unique sessions identify dynamically upon render through random local GUI hashes, treating all demos as "valid" immediately jumping straight to the problem set. 
