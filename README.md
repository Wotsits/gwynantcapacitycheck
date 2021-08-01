# gwynantcapacitycheck
This script scrapes the booking system to obtain the pax of each day.  It this returns a report to highlight any days nearing capacity, any days requiring implementation of a 
stop-sell or any days which have been stop-selled but have since dropped below the capacity threshold and therefore require removal of the stopsell.  

The campsite I manage operates on a pax limit basis but the booking system we use operates on a pitch limit basis.  This presents a challenge - how can we stop taking 
bookings once we reach our limit.  I used to manually check the numbers twice a day.  This was time-consuming.  So to solve the problem, I set up this script.  I run it 
each morning and evening and it alerts me if a stop sell needs implementing on any given date.  
