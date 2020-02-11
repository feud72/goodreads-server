<?php
/* This script allows you to receive data from forms to your email */
if (!empty($_POST))
	{

		/* SETTINGS */

		// email "subject"
		$title = 'New message from my Landing page';
		// email field "From" - name of sender (e.g. your first & last name)
		$from_name = "John Jonson";
		// email field "From" - email of sender (e.g. "robot@domain.com")
		$from_email = "robot@domain.com";
		// Email to receive message - PUT YOUR EMAIL HERE
		$to = "my@email.com";
		// MailChimp integration: Your API key 
		//(leave string empty if you don't want to use MailChimp integration or get your API key there: https://mailchimp.com/help/about-api-keys/)
		$MailChimpAPIkey = '';
		// MailChimp integration: ID of list where your subscribers will be added to
		//(leave string empty if you don't want to use MailChimp integration or get ID of list there: https://us3.admin.mailchimp.com/lists/)
		$MailChimpListID = '';
		
		/* END OF SETTINGS */
		
		$subject = $title;
		$headers = "Content-Type: text/html; charset=UTF-8\r\n";
		$headers .= "From: \"".$from_name."\" <".$from_email.">\r\n";
		$headers .= "Reply-To: \"".$from_name."\" <".$from_email.">\r\n";
		$message = $title."<br>";

		/* FORM FIELDS */
		// if you added some more fields to form, you should add them here too. $_POST["foo"] = <input name="foo" /> or <select name="foo"> or <textarea name="foo">
		
		if(!empty($_POST['name'])){
			$message .= "<b>Name:</b> ".$_POST['name'].'<br />';
			$MailChimpContact["FNAME"] = $_POST['name'];
		}					
		if(!empty($_POST['firstname'])){
			$message .= "<b>First Name:</b> ".$_POST['firstname'].'<br />';
			$MailChimpContact["FNAME"] = $_POST['firstname'];
		}					
		if(!empty($_POST['lastname'])){
			$message .= "<b>Last Name:</b> ".$_POST['lastname'].'<br />';
			$MailChimpContact["LNAME"] = $_POST['lastname'];
		}					
		if(!empty($_POST['phone'])){
			$message .= "<b>Phone:</b> ".$_POST['phone'].'<br />';
			$MailChimpContact["PHONE"] = $_POST['phone'];
		}				
		if(!empty($_POST['email'])){
			$message .= "<b>E-mail:</b> ".$_POST['email'].'<br />';
		}				
		if(!empty($_POST['username'])){
			$message .= "<b>Username:</b> ".$_POST['username'].'<br />';
			$MailChimpContact["FNAME"] = (empty($MailChimpContact["FNAME"]))?$_POST['username']:NULL;
		}				
		if(!empty($_POST['username2'])){
			$message .= "<b>Username:</b> ".$_POST['username2'].'<br />';
			$MailChimpContact["LNAME"] = (empty($MailChimpContact["LNAME"]))?$_POST['username2']:NULL;
		}				
		if(!empty($_POST['password'])){ 	$message .= "<b>Password:</b> ".$_POST['password'].'<br />';	}				
		if(!empty($_POST['password2'])){ 	$message .= "<b>Password:</b> ".$_POST['password2'].'<br />';	}				
		if(!empty($_POST['budget'])){ 		$message .= "<b>Budget:</b> ".$_POST['budget'].'<br />';	}				
		if(!empty($_POST['company_size'])){ $message .= "<b>Company Size:</b> ".$_POST['company_size'].'<br />';	}				
		if(!empty($_POST['card'])){ 		$message .= "<b>Card Number:</b> ".$_POST['card'].'<br />';	}				
		if(!empty($_POST['exp'])){ 			$message .= "<b>Expiration date:</b> ".$_POST['exp'].'<br />';	}				
		if(!empty($_POST['cvv'])){ 			$message .= "<b>CVV:</b> ".$_POST['cvv'].'<br />';	}				
		if(!empty($_POST['zip'])){
			$message .= "<b>ZIP code:</b> ".$_POST['zip'].'<br />';
			$MailChimpContact["ADDRESS"]['zip'] = $_POST['zip'];
		}				
		if(!empty($_POST['country'])){
			$message .= "<b>Country:</b> ".$_POST['country'].'<br />';
			$MailChimpContact["ADDRESS"]['country'] = $_POST['country'];
		}				
		if(!empty($_POST['city'])){
			$message .= "<b>City:</b> ".$_POST['city'].'<br />';
			$MailChimpContact["ADDRESS"]['city'] = $_POST['city'];
		}				
		if(!empty($_POST['address'])){
			$message .= "<b>Address:</b> ".$_POST['address'].'<br />';
			$MailChimpContact["ADDRESS"]['addr1'] = $_POST['address'];
		}				
		if(!empty($_POST['message'])){ 		$message .= "<b>Message:</b> ".str_replace("\n", "<br />", $_POST['message']).'<br />'; }
		if(!empty($_POST['send_copy'])){ 	$message .= "<b>User checked field:</b> Send me a copy<br />";	}				
		if(!empty($_POST['remember'])){ 	$message .= "<b>User checked field:</b> Remember me<br />";	}				
		if(!empty($_POST['rules'])){ 		$message .= "<b>User checked field:</b> I agree to the Terms of Service<br />";	}				
		if(!empty($_POST['method'])){ 		$message .= "<b>Payment method:</b> ".$_POST['method'].'<br />';	}				
		if(!empty($_POST['coupon'])){ 		$message .= "<b>Coupon code:</b> ".$_POST['coupon'].'<br />';	}				
		
		/* END OF FORM FIELDS */
		
		$res = mail($to, $subject, $message, $headers);
		
		/* INTEGRATION WITH MAILCHIMP */
		
		if($MailChimpAPIkey!="" && $MailChimpListID!="" && !empty($_POST['email'])){
			$MailChimpSubdomain = explode("-",$MailChimpAPIkey)[1];
			$MailChimpRequestUrl = 'https://'.$MailChimpSubdomain.'.api.mailchimp.com/3.0/lists/'.$MailChimpListID.'/members/';
			
			// The data to send to the API
			if(!empty($MailChimpContact["ADDRESS"])){
				// Check required fields for address, they should not be empty
				if(empty($MailChimpContact["ADDRESS"]["addr1"])) $MailChimpContact["ADDRESS"]["addr1"]='Address not set';
				if(empty($MailChimpContact["ADDRESS"]["city"])) $MailChimpContact["ADDRESS"]["city"]='City not set';
				if(empty($MailChimpContact["ADDRESS"]["state"])) $MailChimpContact["ADDRESS"]["state"]='State not set';
				if(empty($MailChimpContact["ADDRESS"]["zip"])) $MailChimpContact["ADDRESS"]["zip"]='ZIP not set';
			}
			$SubscriberData = array(
				"email_address" => $_POST['email'], 
				"status" => "subscribed", 
				"merge_fields" => $MailChimpContact,
			);

			// Setup cURL
			$ch = curl_init($MailChimpRequestUrl);
			curl_setopt_array($ch, array(
				CURLOPT_POST => TRUE,
				CURLOPT_RETURNTRANSFER => TRUE,
				CURLOPT_HTTPHEADER => array(
					'Authorization: apikey '.$MailChimpAPIkey,
					'Content-Type: application/json'
				),
				CURLOPT_POSTFIELDS => json_encode($SubscriberData),
			));
			// Send the request
			$response = curl_exec($ch);
		}
		
		/* END OF INTEGRATION WITH MAILCHIMP */
		
		echo 'ok';	
		
	}else{
		echo 'error';
	}
		
?>