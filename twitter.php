<?php
require_once('tmhOAuth/tmhOAuth.php');

exec("python awfuljokes.py", $tweet_text);

$connection = new tmhOAuth(array(
	'consumer_key'    => $consumer_key,
	'consumer_secret' => $consumer_secret,
	'user_token'      => $user_token,
	'user_secret'     => $user_secret,
));

$code = $connection->request("POST", $connection->url("1/statuses/update"), array(
	'status'	=>	$tweet_text[0]
	)
);
?>
