## Crackme2 - A challenge involving a bad RNG design.
***
Can you log in and find the_real_secret?
<br>

### Solution
***
On close inspection of the code, you'll notice that the datetime string used to seed the RNG that creates the key for the JWT signing is not actually variable - it always returns the same date. Once you notice this, the solution becomes trivial.
<br>
A script to quickly create a signed JWT is in `the-solution.py`.
<br>
<br>
<sup>Aaryan.D (aaryan@aary.dev) 2024</sup>
