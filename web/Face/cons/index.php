<?php
	require_once( 'utils.php' );

	$error = "";

	session_unset();

	$db_connection = connect_to_database();
?>

<html>
	<head>
		<title>
			Upcoming conventions
		</title>
	</head>
	<?php include( '../../Common/header.html' ); ?>

		<p><h1 align=center>Upcoming Conventions</h1></p>

		<P align=center>
			<B>You can add or modify a convention on this list via the <A HREF="login.php">Convention Information Manager.</A></B>
		</P>

		<?php
			$result = query_sql( get_convention_details_sql()
					. "where t1.country_id = t2.id and end_date > current_date() "
					. "and approved = true order by day_count", $db_connection );

			$row = mysql_fetch_array( $result );

			$month_number = $row[ 'end_month' ];

			$month_name[ 1 ] = 'January';
			$month_name[ 2 ] = 'February';
			$month_name[ 3 ] = 'March';
			$month_name[ 4 ] = 'April';
			$month_name[ 5 ] = 'May';
			$month_name[ 6 ] = 'June';
			$month_name[ 7 ] = 'July';
			$month_name[ 8 ] = 'August';
			$month_name[ 9 ] = 'September';
			$month_name[ 10 ] = 'October';
			$month_name[ 11 ] = 'November';
			$month_name[ 12 ] = 'December';

			$jump_months = 6;

			echo( '<P align=center>Jump to: ' );

			for ( $month_counter = 0; $month_counter < $jump_months; $month_counter++ )
			{
				$month_number++;

				if ( $month_number == 13 )
				{
					$month_number = 1;
				}

				echo( '<A HREF="#month_' . $month_name[ $month_number ] . '">' );
				echo( $month_name[ $month_number ] . '</A> ' );
			}

			echo( '</P>' );

			$month_number = $row[ 'end_month' ];
			$month_counter = 0;
		?>

		<P><table border>

			<?php
				$week_start = 730488;

				while ( $row )
				{
					$title_row = false;

					while ( $week_start < $row[ 'day_count' ] )
					{
						$title_row = true;
						$week_start = $week_start + 7;
					}

					if ( $title_row )
					{
						$date_result = query_sql( 'select date_format( from_days( ' 
							. $week_start . ' - 3 ), "%W %D %M %Y" ) as date', $db_connection );

						$date_row = mysql_fetch_array( $date_result );

						$saturday_date = $date_row[ 'date' ];

						mysql_free_result( $date_result );

						echo( "<tr align=center>" );

						$close_name = 0;

						echo( "<td bgcolor=black><B><font color=white>" );
						
						while ( ( $month_number != $row[ 'end_month' ] )
							 && ( $month_counter < $jump_months ) )
						{
							$month_counter++;
							$month_number++;

							if ( $month_number == 13 )
							{
								$month_number = 1;
							}

							echo( '<A NAME="month_' . $month_name[ $month_number ] . '">' );

							$close_name++;
						}

						echo( "Europe" );
						
						for ( $close_counter = 0; $close_counter < $close_name; $close_counter++ )
						{
							echo( '</A>' );
						}

						echo( "</font></B></td>" );
						echo( "<td bgcolor=black><B><font color=white>N.&nbsp;America</font></B></td>" );
						echo( "<td bgcolor=black><B><font color=white>Downunder</font></B></td>" );
						echo( "<td bgcolor=black><B><font color=white>Rest&nbsp;World</font></B></td>" );
						echo( "<td bgcolor=black><B><font color=white>Weekend of " . $saturday_date . "</font></B></td>" );


						echo( "</tr>" );
					}

					echo ("<tr>");

					$continent = $row[ 'continent_id' ];

					if ( $continent > 4 )
					{
						$continent = 4;
					}

					for ( $column = 1; $column < $continent; $column++ )
					{
						echo( "<td></td>" );
					}

					echo( "<td align=center>" );

					if ( $row[ 'flag_file' ] == null )
					{
						echo( '<img src="flags/no_flag.gif">' );
					}
					else
					{
						echo( '<img border=1 src="flags/' . $row[ 'flag_file' ] . '">' );
					}

					echo( "</td>" );

					for ( $column = $continent; $column < 4; $column++ )
					{
						echo( "<td></td>" );
					}

					echo( "<td>" );

					echo( "<P><h2 align=center>" );
					
					echo( $row[ 'name' ] );

					echo( "</h2></P>" );

					echo( "<P align=center><B>" . $row[ 'start_date' ] . " - " 
							. $row[ 'end_date' ] . "</B></P>" );

					echo( "<P align=center><B>" . $row[ 'location' ] . ", " 
							. $row[ 'country_name' ] . "</B></P>" );

					echo( "<P>" );

					if ( $row[ 'contact' ] <> "" )
					{
						echo( "Contact: " );

						if ( $row[ 'email' ] <> "" )
						{
							echo( '<A HREF="send_email.php?id=' . $row[ 'id' ] . '">' );
						}
						
						$contact = remove_backslashes( $row[ 'contact' ], false );

						echo( "<B>" . $contact . "</B>" );

						if ( $row[ 'email' ] <> "" )
						{
							echo( '</A>' );
						}

						echo( "<BR/>" );
					}

					if ( $row[ 'url' ] <> "" )
					{
						echo( 'Website: <B><A HREF="' . $row[ 'url' ] . '">' 
								. $row[ 'url' ] . '</A></B><BR/>' );
					}

					if ( $row[ 'comments' ] != "" )
					{
						$comments = remove_backslashes( $row[ 'comments' ], true );

						echo( "</P><P>" );

						echo( $comments );
					}

					echo( "</P>" );

					echo( "</td></tr>" );

					$row = mysql_fetch_array( $result );
				}

				mysql_free_result( $result );

				mysql_close( $db_connection );
			?>
		</table></P>

		<P align=center>
			<B>You can add or modify a convention on this list via the <A HREF="login.php">Convention Information Manager.</A></B>
		</P>

		<?php include( '../Common/footer.html' ); ?>
	</body>
</html>
