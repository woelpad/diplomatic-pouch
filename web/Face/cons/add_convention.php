<?php
	session_start();

	require_once( 'utils.php' );

	$error = "";

	$db_connection = connect_to_database();

	check_page( "", 0, $db_connection );

	$name = "";
	$country = "";
	$url = "http://";
	$syear = "yyyy";
	$smonth = "mm";
	$sday = "dd";
	$eyear = "yyyy";
	$emonth = "mm";
	$eday = "dd";
	$location = "";
	$contact = "";
	$comments = "";
	$email = "";

	if ( isset( $_POST[ 'name' ] ) )
	{
		$name = $_POST[ 'name' ];
		$country = $_POST[ 'country' ];
		$url = $_POST[ 'url' ];
		$syear = $_POST[ 'syear' ];
		$smonth = $_POST[ 'smonth' ];
		$sday = $_POST[ 'sday' ];
		$eyear = $_POST[ 'eyear' ];
		$emonth = $_POST[ 'emonth' ];
		$eday = $_POST[ 'eday' ];
		$location = $_POST[ 'location' ];
		$contact = $_POST[ 'contact' ];
		$comments = $_POST[ 'comments' ];
		$email = $_POST[ 'email' ];

		if ( $name == "" )
		{
			$error = "You must enter the convention name";
		}
		else if ( $country == 0 )
		{
			$error = "You must select a country";
		}
		else
		{
			$result = query_sql("select * from user where id = '" . $_SESSION[ 'user_id' ] . "'",
						$db_connection );

			$row = mysql_fetch_array( $result );

			if ( $row[ 'rights_modify' ] )
			{
				$approved = "true";
			}
			else
			{
				$approved = "false";
			}

			if ( $url == "http://" )
			{
				$url = "";
			}

			mysql_free_result( $result );

			$new_key = get_new_key( "convention", $db_connection );
			$sql_query = "insert into convention values ( " . $new_key . ", '";
			$sql_query = $sql_query . mysql_real_escape_string( $name, $db_connection ) . "', '";
			$sql_query = $sql_query . $syear . '-' . $smonth . '-' . $sday . "', '";
			$sql_query = $sql_query . $eyear . '-' . $emonth . '-' . $eday . "', '";
			$sql_query = $sql_query . mysql_real_escape_string( $location, $db_connection ) . "', '";
			$sql_query = $sql_query . $country . "', '";
			$sql_query = $sql_query . mysql_real_escape_string( $contact, $db_connection ) . "', '";
			$sql_query = $sql_query . mysql_real_escape_string( $comments, $db_connection ) . "', '";
			$sql_query = $sql_query . mysql_real_escape_string( $email, $db_connection ) . "', '";
			$sql_query = $sql_query . mysql_real_escape_string( $url, $db_connection );
			$sql_query = $sql_query . "', null, false, " . $approved . ")";

			$result = mysql_query( $sql_query, $db_connection );

			if ( $result == false )
			{
				$error = "Invalid convention details";

				echo ( $sql_query );
			}
			else
			{
				$sql_query = "insert into log values ( " . $_SESSION[ 'user_id' ] . ", ";
				$sql_query = $sql_query . $new_key . ", now(), ";

				if ( $row[ 'rights_modify' ] )
				{
					$sql_query = $sql_query . "'Convention added with auto-approval', '' )";
				}
				else
				{
					$sql_query = $sql_query . "'Convention added', '' )";
				}

				$result = query_sql( $sql_query, $db_connection );

				if ( $row[ 'rights_modify' ]  == false )
				{
					notify_reviewers( $db_connection );
				}

				goto_page( 'maintain.php' );
			}
		}
	}
?>

<html>
	<head>
		<title>
			Add Convention
		</title>
	</head>
	<body>
		<?php
			report_error( $error );
		?>

		<p><h1>Add a new convention to the database</h1></p>

		<form action="<?php link_to_self(); ?>" method="post">
			<table>
				<tr>
					<td>Name</td>
					<td>
						<input type="text" name="name" value="<?php echo( $name ); ?>" size=60>
					</td>
				</tr>
				<tr>
					<td>Start Date</td>
					<td>
						<input type="text" name="syear" value="<?php echo( $syear ); ?>" size=4>
						<input type="text" name="smonth" value="<?php echo( $smonth ); ?>" size=2>
						<input type="text" name="sday" value="<?php echo( $sday ); ?>" size=2>
					</td>
				</tr>
				<tr>
					<td>End Date</td>
					<td>
						<input type="text" name="eyear" value="<?php echo( $eyear ); ?>" size=4>
						<input type="text" name="emonth" value="<?php echo( $emonth ); ?>" size=2>
						<input type="text" name="eday" value="<?php echo( $eday ); ?>" size=2>
					</td>
				</tr>
				<tr>
					<td>Country</td>
					<td>
						<select name="country">
							<option value="0">--- Select Country ---</option>
							<?php
								$result = query_sql( "select * from country "
										. "order by name", $db_connection );

								$row = mysql_fetch_array( $result );

								while ( $row )
								{
									echo( '<option value="' . $row[ 'id' ] . '"' );

									if ( $row[ 'id' ] == $country )
									{
										echo( ' selected' );
									}
									
									echo( '>' );
									echo( $row[ 'name' ] );
									echo( '</option>' );

									$row = mysql_fetch_array( $result );
								}

								mysql_free_result( $result );
							?>
						</select>

						<?php
							if ( check_rights( "rights_maintain", 0, $db_connection ) )
							{
								echo( '<A HREF="add_country.php">Add a Country</A>' );
							}
						?>
					</td>
				</tr>
				<tr>
					<td>Location</td>
					<td>
						<input type="text" name="location" value="<?php echo( $location ); ?>" size=60><br/>
						Please do not include the country in the location field.
					</td>
				</tr>
				<tr>
					<td>Contact Name</td>
					<td>
						<input type="text" name="contact" value="<?php echo( $contact ); ?>" size=60>
					</td>
				</tr>
				<tr>
					<td>E-Mail</td>
					<td>
						<input type="text" name="email" value="<?php echo( $email ); ?>" size=60>
					</td>
				</tr>
				<tr>
					<td>Website</td>
					<td>
						<input type="text" name="url" value="<?php echo( $url ); ?>" size=60>
					</td>
				</tr>
				<tr valign="top">
					<td>Comments</td>
					<td>
						<textarea name="comments" cols="60" rows="10"><?php echo( $comments ); ?></textarea>
					</td>
				</tr>
				<tr>
					<td></td>
					<td>
						<input type="submit" name="Submit" value="Add Convention">
					</td>
				</tr>
			</table>
		</form>
	</body>
</html>

<?php
	mysql_close( $db_connection );
?>
