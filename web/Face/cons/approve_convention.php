<?php
	session_start();

	require_once( 'utils.php' );

	$error = "";

	$db_connection = connect_to_database();

	check_page( "rights_approve", $_GET[ 'con_id' ], $db_connection );
?>

<html>
	<head>
		<title>
			Approve Convention
		</title>
	</head>
	<body>
		<p><h1 align=center>Approve Convention</h1></p>

		<P><table border>
			<?php
				$result = query_sql( get_convention_details_sql()
						. "where t1.country_id = t2.id and t1.id = " . $_GET[ 'con_id' ], 
						$db_connection );

				$row = mysql_fetch_array( $result );

				if ( $row )
				{
					echo( "<tr align=center>" );
					echo( "<td>Europe</td>" );
					echo( "<td>N.&nbsp;America</td>" );
					echo( "<td>Downunder</td>" );
					echo( "<td>Rest&nbsp;World</td>" );
					echo( "<td>Description</td>" );
					echo( "</tr>" );

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

					echo( "<td>" );

					if ( $row[ 'flag_file' ] == null )
					{
						echo( '<img src="flags/no_flag.gif">' );
					}
					else
					{
						echo( '<img src="flags/' . $row[ 'flag_file' ] . '">' );
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
						echo( "Contact: <B>" . $row[ 'contact' ] . "</B><BR/>" );
					}
					
					if ( $row[ 'email' ] <> "" )
					{
						echo( 'E-mail: <B><A HREF="mailto:' . $row[ 'email' ] . '">' . $row[ 'email' ] . '</A></B><BR/>' );
					}

					if ( $row[ 'url' ] <> "" )
					{
						echo( 'Website: <B><A HREF="' . $row[ 'url' ] . '">' 
								. $row[ 'url' ] . '</A></B><BR/>' );
					}

					if ( $row[ 'comments' ] != "" )
					{
						echo( "</P><P>" );

						echo( $row[ 'comments' ] );
					}

					echo( "</P>" );

					echo( "</td></tr>" );

					$modified_from = $row[ 'modified_from' ];

					$row = mysql_fetch_array( $result );
				}
				else
				{
					mysql_free_result( $result );

					mysql_close( $db_connection );

					goto_page( "maintain.php" );
				}

				mysql_free_result( $result );
			?>
		</table></P>

		<P><table border><tr><td><h2>
			<?php
				link_to_page_with_params( "do_approve.php", "con_id=" . $_GET[ 'con_id' ], "Approve" );
				echo( "</h2></td><td><h2>" );
				link_to_page_with_params( "reject_approve.php", "con_id=" . $_GET[ 'con_id' ], "Reject" );
			?>
		</h2></td></tr></table></P>

		<p><h1 align=center>Change Log</h1></p>

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
						. "and ( convention_id = " . $_GET[ 'con_id' ];

				if ( $modified_from > 0 )
				{
					$sql = $sql . " or convention_id = " . $modified_from;
				}

				$sql = $sql . " ) order by log_date desc";

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

				mysql_close( $db_connection );
			?>
		</table></P>
	</body>
</html>
