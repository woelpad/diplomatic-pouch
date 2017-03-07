<?php
	session_start();

	require_once( 'utils.php' );

	$error = "";

	$db_connection = connect_to_database();

	check_page( "", 0, $db_connection );

	if ( isset( $_POST[ 'name' ] ) )
	{
		if ( $_POST[ 'name' ] == "" )
		{
			$error = "You must enter the convention name";
		}
		else
		{
			$result = query_sql("select * from user where id = '" . $_SESSION[ 'user_id' ] . "'",
						$db_connection );

			$row = mysql_fetch_array( $result );

			if ( $row[ 'rights_modify' ] )
			{
				$approved = true;
			}
			else
			{
				$approved = false;
			}

			mysql_free_result( $result );

			if ( $approved == false )
			{
				$result = query_sql("select * from rights where user_id = '" 
						. $_SESSION[ 'user_id' ] . "' and convention_id = '" 
						. $_GET[ 'con_id' ] . "'", $db_connection );

				$row = mysql_fetch_array( $result );

				if ( $row[ 'rights_modify' ] )
				{
					$approved = true;
				}

				mysql_free_result( $result );
			}

			if ( $approved == true )
			{
				$sql_query = "update convention "
						. "set name='" . mysql_real_escape_string( $_POST[ 'name' ], $db_connection ) . "', "
						. "start_date='" . $_POST[ 'syear' ] . '-' . $_POST[ 'smonth' ] . '-'
						. $_POST[ 'sday' ] . "', "
						. "end_date='" . $_POST[ 'eyear' ] . '-' . $_POST[ 'emonth' ] . '-'
						. $_POST[ 'eday' ] . "', "
						. "location='" . mysql_real_escape_string( $_POST[ 'location' ], $db_connection ) . "', "
						. "country_id='" . $_POST[ 'country' ] . "', "
						. "contact='" . mysql_real_escape_string( $_POST[ 'contact' ], $db_connection ) . "', "
						. "comments='" . mysql_real_escape_string( $_POST[ 'comments' ], $db_connection ) . "', "
						. "email='" . mysql_real_escape_string( $_POST[ 'email' ], $db_connection ) . "', "
						. "url='" . mysql_real_escape_string( $_POST[ 'url' ], $db_connection ) 
						. "', modified_from=null, cancelled=false, approved=true "
						. "where id = " . $_GET[ 'con_id' ];

				$result = mysql_query( $sql_query, $db_connection );

				if ( $result == false )
				{
					$error = "Invalid convention details";

					echo ( $sql_query );
				}
				else
				{
					$sql_query = "insert into log values ( " . $_SESSION[ 'user_id' ] . ", "
							. $_GET[ 'con_id' ] . ", now(), " . "'Convention modified with auto-approval', '" 
							. mysql_real_escape_string( $_POST[ 'mod_comments' ], $db_connection ) 
							. "' )";

					$result = query_sql( $sql_query, $db_connection );

					mysql_close( $db_connection );

					goto_page( 'maintain.php' );
				}
			}
			else
			{
				$new_key = get_new_key( "convention", $db_connection );
				$sql_query = "insert into convention values ( " . $new_key . ", '"
						. mysql_real_escape_string( $_POST[ 'name' ], $db_connection ) . "', '"
						. $_POST[ 'syear' ] . '-' . $_POST[ 'smonth' ] . '-'
						. $_POST[ 'sday' ] . "', '"
						. $_POST[ 'eyear' ] . '-' . $_POST[ 'emonth' ] . '-'
						. $_POST[ 'eday' ] . "', '"
						. mysql_real_escape_string( $_POST[ 'location' ], $db_connection ) . "', '"
						. $_POST[ 'country' ] . "', '"
						. mysql_real_escape_string( $_POST[ 'contact' ], $db_connection ) . "', '"
						. mysql_real_escape_string( $_POST[ 'comments' ], $db_connection ) . "', '"
						. mysql_real_escape_string( $_POST[ 'email' ], $db_connection ) . "', '"
						. mysql_real_escape_string( $_POST[ 'url' ], $db_connection )
						. "', " . $_GET[ 'con_id' ] . ", false, false )";

				$result = mysql_query( $sql_query, $db_connection );

				if ( $result == false )
				{
					$error = "Invalid convention details";

					echo ( $sql_query );
				}
				else
				{
					$sql_query = "insert into log values ( " . $_SESSION[ 'user_id' ] . ", "
							. $new_key . ", now(), " . "'Convention modified', '" 
							. mysql_real_escape_string( $_POST[ 'mod_comments' ], $db_connection ) 
							. "' )";

					$result = query_sql( $sql_query, $db_connection );

					notify_reviewers( $db_connection );

					mysql_close( $db_connection );

					goto_page( 'maintain.php' );
				}
			}
		}
	}
?>

<html>
	<head>
		<title>
			Modify Convention
		</title>
	</head>
	<body>
		<?php
			report_error( $error );

			$result = query_sql( get_convention_details_sql() 
					. "where t1.country_id = t2.id and t1.id = " . $_GET[ 'con_id' ], 
					$db_connection );

			$row = mysql_fetch_array( $result );
		?>

		<p><h1>Modify a convention</h1></p>

		<form action="<?php link_to_self_with_params( 'con_id=' . $_GET[ 'con_id' ] ); ?>" method="post">
			<table>
				<tr>
					<td>Name</td>
					<td>
						<?php
							form_input( "name", $row[ 'name' ], 60 );
						?>
					</td>
				</tr>
				<tr>
					<td>Start Date</td>
					<td>
						<?php
							form_input( "syear", $row[ 'start_year' ], 4 );
							form_input( "smonth", $row[ 'start_month' ], 2 );
							form_input( "sday", $row[ 'start_day' ], 2 );
						?>
					</td>
				</tr>
				<tr>
					<td>End Date</td>
					<td>
						<?php
							form_input( "eyear", $row[ 'end_year' ], 4 );
							form_input( "emonth", $row[ 'end_month' ], 2 );
							form_input( "eday", $row[ 'end_day' ], 2 );
						?>
					</td>
				</tr>
				<tr>
					<td>Country</td>
					<td>
						<select name="country">
							<?php
								$counties = query_sql( "select * from country "
										. "order by name", $db_connection );

								$country = mysql_fetch_array( $counties );

								while ( $country )
								{
									echo( '<option value="' . $country[ 'id' ] . '"' );
									
									if ( $country[ 'id' ] == $row[ 'country_id' ] )
									{
										echo( ' selected="selected"' );
									}
									
									echo ( '>' );
									echo( $country[ 'name' ] );
									echo( '</option>' );

									$country = mysql_fetch_array( $counties );
								}

								mysql_free_result( $counties );
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
						<?php
							form_input( "location", $row[ 'location' ], 60 );
						?>
					</td>
				</tr>
				<tr>
					<td>Contact Name</td>
					<td>
						<?php
							$contact = remove_backslashes( $row[ 'contact' ], false );

							form_input( "contact", $contact, 60 );
						?>
					</td>
				</tr>
				<tr>
					<td>E-Mail</td>
					<td>
						<?php
							form_input( "email", $row[ 'email' ], 60 );
						?>
					</td>
				</tr>
				<tr>
					<td>Website</td>
					<td>
						<?php
							form_input( "url", $row[ 'url' ], 60 );
						?>
					</td>
				</tr>
				<tr valign="top">
					<td>Comments</td>
					<td>
						<?php
							echo( '<textarea name="comments" cols="60" rows="10">' );

							$comments = remove_backslashes( $row[ 'comments' ], false );

							echo( $comments );

							echo( '</textarea>' );
						?>
					</td>
				</tr>
				<tr>
					<td>Reason for<br>modification</td>
					<td>
						<?php
							form_input( "mod_comments", "", 60 );
						?>
					</td>
				</tr>
				<tr>
					<td></td>
					<td>
						<input type="submit" name="Submit" value="Modify">
					</td>
				</tr>
			</table>
		</form>

		<p><h1>Change Log</h1></p>

		<P><table border>
			<tr>
				<td>Name</td>
				<td>Date</td>
				<td>Action</td>
				<td>Comment</td>
			</tr>
			<?php
				$sql = "select t1.username, t1.password, t1.name, t1.email, t2.user_id, "
						. "t2.convention_id, t2.log_date, t2.action, t2.comment "
						. "from user as t1, log as t2 where t1.id = t2.user_id "
						. "and convention_id = " . $_GET[ 'con_id' ]
						. " order by log_date desc";

				$result = query_sql( $sql, $db_connection );

				$row = mysql_fetch_array( $result );

				while ( $row != "" )
				{
					echo( "<tr>" );
					echo( "<td>" . $row[ 'name' ] . "</td>" );
					echo( "<td>" . $row[ 'log_date' ] . "</td>" );
					echo( "<td>" . $row[ 'action' ] . "</td>" );
					echo( "<td>" . $row[ 'comment' ] . "</td>" );
					echo( "</tr>" );

					$row = mysql_fetch_array( $result );
				}
			?>
		</table></P>
	</body>
</html>

<?php
	mysql_close( $db_connection );
?>
