<?php
if ($_POST) {
	$dest = 'woelpad@gmail.com';
	$subject = 'F2017M: New photo comment';
	$options = '-f track@diplomatic-pouch.com';
	$error = '';

	$file = 'identity';
	$identities = file_get_contents($file);
	$identities = $identities ? json_decode($identities) : [];
	$identity = [
		'email' => $_POST['email'],
		'author' => $_POST['author'],
		'initials' => $_POST['initials'],
		'participant' => $_POST['participant'],
	];
	$initials = $identity['initials'];
	$identities[$initials] = $identity;
	file_put_contents($file, json_encode($identities));
	chmod($file, 0666);

    $message =  '<p author="'.htmlspecialchars($_POST['author']).'" initials="'.htmlspecialchars($_POST['initials']).'" email="'.htmlspecialchars($_POST['email']).'" participant="'.$_POST['participant'].'" photo="'.$_POST['photo'].'">'.htmlspecialchars($_POST['comment']).'</p>'.PHP_EOL;
	
	$file = 'permission';
	$inform = !file_exists($file);
	if (!file_put_contents($file, $message, FILE_APPEND)) {
		$error = 'Failed to copy comment';
	} else {
		chmod($file, 0666);
	}

	//send email
	if ($error) {
		$inform = true;
		$subject .= ' ('.$error.')'; 
	}
	if ($inform) {
		if (mail($dest, $subject, $message, '', $options)) {
			http_response_code(200);
		} else {
			http_response_code(500);
			echo "Failed to inform the author. Please contact ".$dest." separately with your submissions.";
		}
	}
}
?>
