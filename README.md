# AQS_API_readin
Python code to read in AQS data from the EPA API (https://aqs.epa.gov/aqsweb/documents/data_api.html)

**Before Using you need a login and key**
## Getting Started: 
**1.** Get a login and key <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; https\://<span></span>aqs\.epa\.gov/data/api/signup?email=myemail<span></span>@example\.com  <br/>
&nbsp;&nbsp;&nbsp;&nbsp;a.) Update myemail<span></span>@example\.com to your email  <br/>
&nbsp;&nbsp;&nbsp;&nbsp;b.) Past updated link in address bar of your browser <br/>

**2.** Update **user_info.py** with: 
 - login
 - key
 - preferred directory to save files
 <br/>
 <a/>
 
**3.** Make a **input.py** file (or update an example file) for the data you would like to retrieve <br /> 
&nbsp;&nbsp;&nbsp;&nbsp; Info needed:
 - param
 - bdate (starting date in YYYYMMDD)
 - edate (ending date in YYYYMMDD)
 - state code
 <br/>
 <a/>
 
**4.** Run input.py <br/>


### State Codes
<table>
<thead>
<tr>
<th>State Name</th>
<th>State Code</th>
</tr>
</thead>
<tbody>
<tr>
<td>Alabama</td>
<td>01</td>
</tr>
<tr>
<td>Alaska</td>
<td>02</td>
</tr>
<tr>
<td>Arizona</td>
<td>04</td>
</tr>
<tr>
<td>Arkansas</td>
<td>05</td>
</tr>
<tr>
<td>California</td>
<td>06</td>
</tr>
<tr>
<td>Colorado</td>
<td>08</td>
</tr>
<tr>
<td>Connecticut</td>
<td>09</td>
</tr>
<tr>
<td>Delaware</td>
<td>10</td>
</tr>
<tr>
<td>District Of Columbia</td>
<td>11</td>
</tr>
<tr>
<td>Florida</td>
<td>12</td>
</tr>
<tr>
<td>Georgia</td>
<td>13</td>
</tr>
<tr>
<td>Hawaii</td>
<td>15</td>
</tr>
<tr>
<td>Idaho</td>
<td>16</td>
</tr>
<tr>
<td>Illinois</td>
<td>17</td>
</tr>
<tr>
<td>Indiana</td>
<td>18</td>
</tr>
<tr>
<td>Iowa</td>
<td>19</td>
</tr>
<tr>
<td>Kansas</td>
<td>20</td>
</tr>
<tr>
<td>Kentucky</td>
<td>21</td>
</tr>
<tr>
<td>Louisiana</td>
<td>22</td>
</tr>
<tr>
<td>Maine</td>
<td>23</td>
</tr>
<tr>
<td>Maryland</td>
<td>24</td>
</tr>
<tr>
<td>Massachusetts</td>
<td>25</td>
</tr>
<tr>
<td>Michigan</td>
<td>26</td>
</tr>
<tr>
<td>Minnesota</td>
<td>27</td>
</tr>
<tr>
<td>Mississippi</td>
<td>28</td>
</tr>
<tr>
<td>Missouri</td>
<td>29</td>
</tr>
<tr>
<td>Montana</td>
<td>30</td>
</tr>
<tr>
<td>Nebraska</td>
<td>31</td>
</tr>
<tr>
<td>Nevada</td>
<td>32</td>
</tr>
<tr>
<td>New Hampshire</td>
<td>33</td>
</tr>
<tr>
<td>New Jersey</td>
<td>34</td>
</tr>
<tr>
<td>New Mexico</td>
<td>35</td>
</tr>
<tr>
<td>New York</td>
<td>36</td>
</tr>
<tr>
<td>North Carolina</td>
<td>37</td>
</tr>
<tr>
<td>North Dakota</td>
<td>38</td>
</tr>
<tr>
<td>Ohio</td>
<td>39</td>
</tr>
<tr>
<td>Oklahoma</td>
<td>40</td>
</tr>
<tr>
<td>Oregon</td>
<td>41</td>
</tr>
<tr>
<td>Pennsylvania</td>
<td>42</td>
</tr>
<tr>
<td>Rhode Island</td>
<td>44</td>
</tr>
<tr>
<td>South Carolina</td>
<td>45</td>
</tr>
<tr>
<td>South Dakota</td>
<td>46</td>
</tr>
<tr>
<td>Tennessee</td>
<td>47</td>
</tr>
<tr>
<td>Texas</td>
<td>48</td>
</tr>
<tr>
<td>Utah</td>
<td>49</td>
</tr>
<tr>
<td>Vermont</td>
<td>50</td>
</tr>
<tr>
<td>Virginia</td>
<td>51</td>
</tr>
<tr>
<td>Washington</td>
<td>53</td>
</tr>
<tr>
<td>West Virginia</td>
<td>54</td>
</tr>
<tr>
<td>Wisconsin</td>
<td>55</td>
</tr>
<tr>
<td>Wyoming</td>
<td>56</td>
</tr>
<tr>
<td>Guam</td>
<td>66</td>
</tr>
<tr>
<td>Puerto Rico</td>
<td>72</td>
</tr>
<tr>
<td>Virgin Islands</td>
<td>78</td>
</tr>
<tr>
<td>Country Of Mexico</td>
<td>80</td>
</tr>
<tr>
<td>Canada</td>
<td>CC</td>
</tr>
</tbody>
</table>

### Criteria Parameter Codes

<table>
<thead>
<tr>
<th>Parameter Name</th>
<th>Parameter Code</th>
</tr>
</thead>
<tbody>
<tr>
<td>Carbon monoxide</td>
<td>42101</td>
</tr>
<tr>
<td>Lead (TSP) LC</td>
<td>14129</td>
</tr>
<tr>
<td>Lead PM10 LC FRM/FEM</td>
<td>85129</td>
</tr>
<tr>
<td>Nitrogen dioxide (NO2)</td>
<td>42602</td>
</tr>
<tr>
<td>Ozone</td>
<td>44201</td>
</tr>
<tr>
<td>PM10 Total 0-10um STP</td>
<td>81102</td>
</tr>
<tr>
<td>PM2.5 - Local Conditions</td>
<td>88101</td>
</tr>
<tr>
<td>Sulfur dioxide</td>
<td>42401</td>
</tr>
</tbody>
</table>
