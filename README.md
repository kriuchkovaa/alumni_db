# alumni_db
Development Log for Alumni Database 

*See associated PDF file for ERD.
"query_preprocessing.py" automates preprocessing of raw queries extracted from Peoplesoft.*

**NOTE: Microsoft Access file is hidden due to privacy considerations.**

List of queries:

1. <details><summary> <b>Alumni Employment Lookup</b>: Checks employment history for specific alumni based on their last names.</summary>

   ```sql
   SELECT Alumni_Employment.StudentID, Alumni_Term_Prog.LastName+' '+Alumni_Term_Prog.FirstName AS [Full Name], Alumni_Term_Prog.GradTerm, Alumni_Employment.Company, Alumni_Employment.Position, Alumni_Employment.LinkedIn
   FROM Alumni_Employment INNER JOIN Alumni_Term_Prog ON Alumni_Employment.StudentID = Alumni_Term_Prog.StudentID
   WHERE (((Alumni_Term_Prog.LastName)=[Enter last name: ]));

</details>

2. <details><summary><b>Boeing Alumni</b>: Shows alumni working at Boeing (Boeing Partnership); use work email domain as a filter.</summary>

    ```sql
   SELECT Alumni_Contact.StudentID, Alumni_Term_Prog.GradTerm, Alumni_Term_Prog.LastName, Alumni_Term_Prog.FirstName, Alumni_Term_Prog.Degree, Alumni_Term_Prog.Plan, Alumni_Term_Prog.[Continuing?], Alumni_Contact.[Personal Email]
   FROM Alumni_Term_Prog INNER JOIN Alumni_Contact ON Alumni_Term_Prog.StudentID = Alumni_Contact.StudentID
   WHERE (((Alumni_Contact.[Personal Email]) Alike '%boeing%'));

</details>

3. <details><summary><b>Faculty Alumni</b>: Display alumni currently employed as associate faculty.</summary>

    ```sql
   SELECT Alumni_Term_Prog.StudentID, Alumni_Term_Prog.GradTerm, Alumni_Term_Prog.LastName, Alumni_Term_Prog.FirstName, Alumni_Term_Prog.Degree AS [Grad Degree], Alumni_Term_Prog.[IsFaculty]
   FROM Alumni_Term_Prog
   WHERE (((Alumni_Term_Prog.[IsFaculty])=Yes));

</details>

4. <details><summary><b>CompanyListSQL</b>: List of companies offering partnership for case studies and class visits.</summary>

    ```sql
   SELECT DISTINCT L.Company
   FROM Company_List AS L INNER JOIN Company_Contacts AS C ON L.Company = C.Company;

</details>

5. <details><summary><b>DBAKingNotFac</b>: Capture DBA alumni currently not employed as associate faculty (allows to look for potential teaching candidates).</summary>

    ```sql
    SELECT Alumni_Term_Prog.StudentID, Alumni_Term_Prog.LastName, Alumni_Term_Prog.FirstName, Alumni_Term_Prog.Degree, Alumni_Contact.[Personal Email], Alumni_Contact.City, Alumni_Contact.State
    FROM Alumni_Term_Prog INNER JOIN Alumni_Contact ON Alumni_Term_Prog.StudentID = Alumni_Contact.StudentID
    WHERE (
            (Alumni_Contact.Zipcode ALIKE '980%' AND Alumni_Contact.Zipcode <> '98000') 
            OR Alumni_Contact.Zipcode ALIKE '981%' 
            OR (Alumni_Contact.Zipcode ALIKE '982%' AND Alumni_Contact.Zipcode NOT ALIKE '9829%')
        )
    AND Alumni_Term_Prog.Degree = 'DBA' 
    AND Alumni_Term_Prog.[CityU Faculty?] = False;

</details>

6. <details><summary><b>DMD_Inductees</b>: Lists alumni inducted into honorary chapter.</summary>

    ```sql
   SELECT Q.StudentID, Q.GradTerm, Q.LastName, Q.FirstName, Q.Degree, Nz(Q.PartnerEmail, C.[Personal Email]) AS [Personal Email], Q.Partner
   FROM Unioned_DMDs AS Q LEFT JOIN Alumni_Contact AS C ON Q.StudentID = C.StudentID;

</details>

7. <details><summary><b>King_County_Alumni</b>: List of local alumni (based in King County) - intended for promotion of onsite events and class visit planning. </summary>

    ```sql
   SELECT Alumni_Term_Prog.StudentID, Alumni_Term_Prog.LastName, Alumni_Term_Prog.FirstName, Alumni_Term_Prog.Degree, Alumni_Contact.[Personal Email], Alumni_Contact.City, Alumni_Contact.State
   FROM Alumni_Term_Prog INNER JOIN Alumni_Contact ON Alumni_Term_Prog.StudentID = Alumni_Contact.StudentID
   WHERE Alumni_Contact.Zipcode Alike '980%' AND Alumni_Contact.Zipcode <> '98000' OR Alumni_Contact.Zipcode Alike '981%' OR Alumni_Contact.Zipcode Alike '982%' AND Alumni_Contact.Zipcode Not Alike '9829%';

</details>

8. <details><summary><b>MBA Graduates</b>: List of MBA graduates - accreditation/reporting. </summary>

      ```sql
      SELECT StudentID, GradTerm, LastName, FirstName, Degree, Plan
      FROM Alumni_Term_Prog
      WHERE Degree="MBA"
      ORDER BY GradTerm DESC; 

</details>

9. <details><summary><b>PotentialFacultyLocal</b>: Displays contacts from partner companies potentially interested in teaching. </summary>

     ```sql
    SELECT [Full Name], Company, Email, LinkedIn, [Highest Credentials]
    FROM Company_Contacts
    WHERE Local = True AND [Interested in Teaching] = True;

</details>

10. <details><summary><b>RecentPMs</b>: Shows alumni, including returning students, with degrees/plans in project management - useful for promoting new PM degrees, as well as PMI partnership event promotion.</summary>
    
    ```sql
    SELECT Alumni_Term_Prog.StudentID, Alumni_Term_Prog.GradTerm, Alumni_Term_Prog.LastName, Alumni_Term_Prog.FirstName, Alumni_Term_Prog.Degree, Alumni_Term_Prog.Plan, Alumni_Term_Prog.[Continuing?], Alumni_Secondary_Degree.Degree AS [Secondary Degree], Alumni_Secondary_Degree.Plan AS [Secondary Plan], Alumni_Secondary_Degree.GradTerm AS [Secondary Grad Term], 
    Alumni_Continuing.Degree AS [Continuing Degree], Alumni_Continuing.Plan AS [Continuing Plan]
    FROM (Alumni_Term_Prog LEFT JOIN Alumni_Secondary_Degree ON Alumni_Term_Prog.StudentID = Alumni_Secondary_Degree.StudentID) LEFT JOIN Alumni_Continuing ON Alumni_Term_Prog.StudentID = Alumni_Continuing.StudentID
    WHERE Alumni_Term_Prog.Degree IN ("BSPM", "MSPM") OR Alumni_Term_Prog.Degree IN ("BSPM", "MSPM")
    ORDER BY Alumni_Term_Prog.GradTerm DESC;

</details>

11. <details><summary><b>Selected Per Location</b>: Captures total number of alumni in each term per most popular programs across specific international campuses.</summary>

       ```sql
      SELECT Q.Degree, Q.GradTerm, Q.Country, Count(*) AS [Total Alumni]
      FROM (SELECT Alumni_Term_Prog.Degree, Alumni_Term_Prog.GradTerm, "US" AS Country
       FROM Alumni_Term_Prog
       WHERE Alumni_Term_Prog.Degree IN ("BAM", "BSBA", "MBA")
   
       UNION ALL
       
       SELECT Alumni_Partner.Degree, Alumni_Partner.GradTerm, Alumni_Partner.Country
       FROM Alumni_Partner
       WHERE Alumni_Partner.Degree IN ("BAM", "BSBA", "MBA")
       AND Alumni_Partner.Country NOT IN ("Canada", "China", "Vietnam")
   )  AS Q
   GROUP BY Q.Degree, Q.GradTerm, Q.Country;
   
   </details>

12. <details><summary><b>Total Alumni Per Program and Term</b>: For capturing retention.</summary>

    ```sql
    SELECT Alumni_Term_Prog.Degree, Alumni_Term_Prog.GradTerm, Count(*) AS [Total Alumni]
    FROM Alumni_Term_Prog
    GROUP BY Alumni_Term_Prog.Degree, Alumni_Term_Prog.GradTerm;

</details>

