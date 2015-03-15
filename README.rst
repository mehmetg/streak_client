.. image:: https://travis-ci.org/mehmetg/streak_client.svg
    :target: https://travis-ci.org/mehmetg/streak_client

=============
streak_client
=============

-------------
Description
-------------

    Python client module for Streak API.
    For more information and documentation please refer to `Streak API Documentation <http://www.streak.com/api>`_.

-------------
Installation
-------------

> pip install streak_client

-------------
Known issues
-------------

    * Does not work with Python 3.x, yet.
    * Unittests are not complete (see dev status)

-------------
TODO
-------------

	* Resolved issues with API methods tagged tested 'unclear'
	* Implement unittests for API methods tagged tested 'manual'

-------------
Tests
-------------

Tests use a dummy gmail account. Feel free to change it with your own. :)

--------------------------
Development Status
--------------------------

	========== ==============================
	Status     Description
	========== ==============================
	manual     Indicates manually verified.
	unittest   Indicates tests implemented.
	unclear    Indicates API issue.
	========== ==============================

------------

	====================== =========== ======== 
	Methods                Implemented Tested   
	====================== =========== ======== 
	**User Methods**                                
	get_user               Yes         *unittest* 
	get_pipeline           Yes         *unittest* 
	delete_pipeline        Yes         *unittest* 
	delete_all_pipelines   Yes         *unittest* 
	create_pipeline        Yes         *unittest* 
	update_pipeline        Yes         *unittest* 
	**Box Methods**                                 
	get_box                Yes         Manual   
	get_pipeline_boxes     Yes         Manual   
	delete_box             Yes         Manual   
	create_pipeline_box    Yes         Manual   
	update_box             Yes         Manual   
	**Search Methods**                              
	search                 Yes         Manual   
	**Snippet Methods**                             
	get_snippet            Yes         Manual   
	**Stage Methods**                               
	get_pipeline_stage     Yes         Manual   
	create_pipeline_stage  Yes         Manual   
	delete_pipeline_stage  Yes         Manual   
	update_pipeline_stage  Yes         Manual   
	**Field Methods**                               
	get_pipeline_field     Yes         Manual   
	create_pipeline_field  Yes         Manual   
	update_pipeline_field  Yes         Manual   
	delete_pipeline_field  Yes         Manual   
	get_box_field          Yes         **Unclear**    
	create_box_field       Yes         **Unclear**    
	update_box_field       Yes         **Unclear**    
	delete_box_field       Yes         **Unclear**    
	**Newsfeed Methods**                            
	get_pipeline_newsfeeds Yes         Manual   
	get_box_newsfeeds      Yes         Manual   
	**Thread Methods**                              
	get_thread             Yes         Manual   
	get_box_threads        Yes         Manual   
	**Comment Methods**                             
	create_box_comments    Yes         Manual   
	get_box_comments       Yes         Manual   
	delete_box_comment     Yes         **Unclear**    
	**Reminder Methods**                            
	create_box_reminder    Yes         Manual   
	update_reminder        Yes         Manual   
	get_box_reminders      Yes         Manual   
	get_reminder           Yes         Manual   
	delete_reminder        Yes         Manual   
	**File Methods**                                
	get_file               Yes         Manual   
	get_file_contents      Yes         **Unclear**  
	get_file_link          Yes         **Unclear**    
	get_box_files          Yes         Manual   
	====================== =========== ======== 
