<?php
	function connect_to_database()
	{
		$db_connection = mysql_connect( "127.0.0.1", "davidn", "convpass" );

		if ( $db_connection == false )
		{
			die( "Error connecting to database" );
		}

		$result = mysql_select_db( "conventions", $db_connection );

		return $db_connection;
	}

	function query_sql( $query, $db_connection )
	{
		$result = mysql_query( $query, $db_connection );

		if ( $result == false )
		{
			echo( 'SQL Query : ' . $query . ' :<P>\n' );
			die( 'MySQL query failed: ' . mysql_error() );
		}

		return $result;
	}

	function check_result( $result )
	{
		if ( $result == false )
		{
			die( 'MySQL query failed: ' . mysql_error() );
		}
	}

	/**
	 * Generate a new primary key for a table, and increment the next key
	 **/

	function get_new_key( $table_name, $db_connection )
	{
		$result = query_sql( "select * from key_counter where table_name = '" . $table_name . "'",
					$db_connection );

		$row = mysql_fetch_array( $result );

		$new_key = $row[ "next_key" ];

		mysql_free_result( $result );

		$result = query_sql( "update key_counter set next_key = " . ( $new_key + 1 ) 
					. " where table_name = '" . $table_name . "'", $db_connection );

		return $new_key;
	}

	function goto_page( $page_filename )
	{
		header("Location:" . $page_filename . "?" . session_name() . "=" . session_id() );
		exit();
	}

	/**
	 * Check user is logged in. Also checks:
	 *
	 *   - user has the specified rights, if rights is not an empty string
	 *
	 *   - rights may be for the user, or the specified convention (if convention_id is not 0)
	 **/

	function check_rights( $rights, $convention_id, $db_connection )
	{
		$ok = false;

		if ( isset( $_SESSION['user_id'] ) )
		{
			if ( $rights == "" )
			{
				$ok = true;
			}
			else
			{
				$result = query_sql( "select * from user where deleted = false and id = " 
						. $_SESSION['user_id'], $db_connection );

				$row = mysql_fetch_array( $result );

				if ( $row )
				{
					if ( $row[ $rights ] )
					{
						// Rights granted
						$ok = true;
					}
					else
					{
						mysql_free_result( $result );

						$result = query_sql( "select * from rights where user_id = " 
								. $_SESSION['user_id'] . " and convention_id = " . $convention_id, 
								$db_connection );

						$row = mysql_fetch_array( $result );

						if ( $row )
						{
							if ( $row[ $rights ] )
							{
								// Rights granted
								$ok = true;
							}
						}
					}
				}

				mysql_free_result( $result );
			}
		}

		return $ok;
	}

	/**
	 * Check the rights, and go to the login page if insufficient
	 **/

	function check_page( $rights, $convention_id, $db_connection )
	{
		$ok = check_rights( $rights, $convention_id, $db_connection );

		if ( $ok == false )
		{
			goto_page( "login.php" );
		}
	}

	function report_error( $error )
	{
		if ( $error != "" )
		{
			echo ( "<P> <font color=#FF0000> " . $error . "</font></P>");
		}
	}

	/** 
	 * Link to this page, for use in forms
	 **/

	function link_to_self()
	{
		echo( $_SERVER[ 'PHP_SELF' ] . "?" . session_name() . "=" . session_id() );
	}

	/** 
	 * Link to this page with params, for use in forms
	 **/

	function link_to_self_with_params( $params )
	{
		echo( $_SERVER[ 'PHP_SELF' ] . "?" . session_name() . "=" . session_id()
				. "&" . $params );
	}

	/**
	 * Link to a specified page
	 **/

	function link_to_page( $address, $link_text )
	{
		echo( '<A HREF="' );
		echo( $address . "?" . session_name() . "=" . session_id() );
		echo( '">' );
		echo( $link_text );
		echo( '</A>' );
	}

	function link_to_page_with_params( $address, $params, $link_text )
	{
		echo( '<A HREF="' );
		echo( $address . "?" . session_name() . "=" . session_id() . "&" . $params );
		echo( '">' );
		echo( $link_text );
		echo( '</A>' );
	}

	function form_input( $name, $value, $width )
	{
		echo( '<input type="text" name="' .$name . '" value="' . $value 
				. '" size=' . $width . '>' );
	}

	function form_checkbox( $name, $value )
	{
		echo( '<input type="checkbox" name="' . $name . ( $value ? '" checked>' : '">' ) );
	}

	function get_convention_details_sql()
	{
		return 'select t1.id, t1.name, date_format( t1.start_date, "%W %D %M %Y" ) as start_date, '
		. 'year( t1.start_date ) as start_year, month( t1.start_date ) as start_month, '
		. 'dayofmonth( t1.start_date ) as start_day, year( t1.end_date ) as end_year, '
		. 'month( t1.end_date ) as end_month, dayofmonth( t1.end_date ) as end_day, '
		. 'date_format( t1.end_date, "%W %D %M %Y" ) as end_date, '
		. 'to_days( t1.start_date ) as day_count, t1.location, t1.country_id, t1.contact, '
		. 't1.comments, t1.email, t1.url, t1.modified_from, t1.cancelled, t1.approved, '
		. 't2.name as country_name, t2.flag_file, t2.continent_id '
		. 'from convention as t1, country as t2 ';
	}

	function notify_reviewers( $db_connection )
	{
		$subject = "Diplomatic Pouch Upcoming Conventions Page";
		$body = "A modification to the Diplomatic Pouch Upcoming Conventions Page\r\n"
			  . "is waiting for approval.\r\n\r\n"
			  . "http://www.diplom.org/Face/cons/login.php\r\n";

		$sql = 'select * from user where id <> ' . $_SESSION[ 'user_id' ] 
			 . ' and notifications < 3 and last_notification < subdate( current_date, 7 )'
			 . ' and deleted = 0 and rights_approve = 1';
		
		$result = query_sql( $sql, $db_connection );

		$row = mysql_fetch_array( $result );

		while ( $row )
		{
			$mail_ok = mail( $row[ 'email' ], $subject, $body );

			if ( $mail_ok )
			{
				$sql = 'update user set notifications = ' . ( $row[ 'notifications' ] + 1 )
					 . ', last_notification = current_date where id = ' . $row[ 'id' ];

				query_sql( $sql, $db_connection );
			}

			$row = mysql_fetch_array( $result );
		}

		mysql_free_result( $result );
	}

	function remove_backslashes( $string, $allow_paragraphs )
	{
		$new_string = str_replace( "\\" . "'", "'", $string );
		$new_string = str_replace( '\"', '"', $new_string );
		$new_string = str_replace( "\r\n", "\n", $new_string );
		$new_string = str_replace( "\r", "\n", $new_string );
		$new_string = str_replace( "\n\n", "\n", $new_string );
		if ( $allow_paragraphs )
		{
			$new_string = str_replace( "\n", "</P><P>", $new_string );
		}
		else
		{
			$new_string = str_replace( "\n", "", $new_string );
		}

		return $new_string;
	}
?>
