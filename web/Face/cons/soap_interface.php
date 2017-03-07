<?php
	// Pull in the NuSOAP code
	require_once( 'nusoap/nusoap.php' );

	// Pull in the util functions
	require_once( 'utils.php' );

	// Create the server instance
	$server = new soap_server();

	// Initialize WSDL support
	$server->configureWSDL( 'conventions', 'urn:conventions' );

	// Register the Data Types
	
	// Continent
	$server->wsdl->addComplexType( 
			'continent',
			'complexType',
			'struct',
			'all',
			'',
			array( 'id' => array( 'name' => 'id', 'type' => 'xsd:int' ),
				   'name' => array( 'name' => 'name', 'type' => 'xsd:string' ) ) );

	// Country
	$server->wsdl->addComplexType( 
			'country',
			'complexType',
			'struct',
			'all',
			'',
			array( 'id' => array( 'name' => 'id', 'type' => 'xsd:int' ),
				   'name' => array( 'name' => 'name', 'type' => 'xsd:string' ),
				   'continent_id' => array( 'name' => 'continent_id', 'type' => 'xsd:int' ),
				   'continent_name' => array( 'name' => 'continent_name', 'type' => 'xsd:string' ),
				   'flag' => array( 'name' => 'flag', 'type' => 'xsd:boolean' ) ) );

	// Convention
	$server->wsdl->addComplexType( 
			'convention',
			'complexType',
			'struct',
			'all',
			'',
			array( 'id' => array( 'name' => 'id', 'type' => 'xsd:int' ),
				   'name' => array( 'name' => 'name', 'type' => 'xsd:string' ),
				   'start_year' => array( 'name' => 'start_year', 'type' => 'xsd:int' ),
				   'start_month' => array( 'name' => 'start_month', 'type' => 'xsd:int' ),
				   'start_month_name' => array( 'name' => 'start_month_name', 'type' => 'xsd:string' ),
				   'start_day' => array( 'name' => 'start_day', 'type' => 'xsd:int' ),
				   'end_year' => array( 'name' => 'end_year', 'type' => 'xsd:int' ),
				   'end_month' => array( 'name' => 'end_month', 'type' => 'xsd:int' ),
				   'end_month_name' => array( 'name' => 'end_month_name', 'type' => 'xsd:string' ),
				   'end_day' => array( 'name' => 'end_day', 'type' => 'xsd:int' ),
				   'location' => array( 'name' => 'location', 'type' => 'xsd:string' ),
				   'country_id' => array( 'name' => 'country_id', 'type' => 'xsd:int' ),
				   'country_name' => array( 'name' => 'country_name', 'type' => 'xsd:string' ),
				   'continent_id' => array( 'name' => 'continent_id', 'type' => 'xsd:int' ),
				   'continent_name' => array( 'name' => 'continent_name', 'type' => 'xsd:string' ),
				   'contact' => array( 'name' => 'contact', 'type' => 'xsd:string' ),
				   'comments' => array( 'name' => 'comments', 'type' => 'xsd:string' ),
				   'email' => array( 'name' => 'email', 'type' => 'xsd:string' ),
				   'url' => array( 'name' => 'url', 'type' => 'xsd:string' ) ) );
	
	// Continent Array
	$server->wsdl->addComplexType(
			'continent_array',
			'complexType',
			'array',
			'',
			'SOAP-ENC:Array',
			array(),
			array( array( 'ref' => 'SOAP-ENC:arrayType', 'wsdl:arrayType' => 'tns:continent[]' ) ),
			'tns:continent' );

	// Country Array
	$server->wsdl->addComplexType(
			'country_array',
			'complexType',
			'array',
			'',
			'SOAP-ENC:Array',
			array(),
			array( array( 'ref' => 'SOAP-ENC:arrayType', 'wsdl:arrayType' => 'tns:country[]' ) ),
			'tns:country' );

	// Convention Array
	$server->wsdl->addComplexType(
			'convention_array',
			'complexType',
			'array',
			'',
			'SOAP-ENC:Array',
			array(),
			array( array( 'ref' => 'SOAP-ENC:arrayType', 'wsdl:arrayType' => 'tns:convention[]' ) ),
			'tns:convention' );

	// Register the Functions

	// Get Continent by ID
	$server->register(
			'get_continent',
			array( 'id' => 'xsd:int' ),
			array( 'return' => 'tns:continent' ),
			'conventions',
			'conventions#get_continent',
			'rpc',
			'encoded',
			'Get a Continent by ID' );

	// Get All Continents. Input parameter is ignored.
	$server->register(
			'get_all_continents',
			array( 'ignore' => 'xsd:int' ),
			array( 'return' => 'tns:continent_array' ),
			'conventions',
			'conventions#get_all_continents',
			'rpc',
			'encoded',
			'Get all Continents' );

	// Get Country by ID
	$server->register(
			'get_country',
			array( 'id' => 'xsd:int' ),
			array( 'return' => 'tns:country' ),
			'conventions',
			'conventions#get_country',
			'rpc',
			'encoded',
			'Get a Country by ID' );

	// Get All Countries. Input parameter is ignored.
	$server->register(
			'get_all_countries',
			array( 'ignore' => 'xsd:int' ),
			array( 'return' => 'tns:country_array' ),
			'conventions',
			'conventions#get_all_countries',
			'rpc',
			'encoded',
			'Get all Countries' );

	// Get Convention by ID
	$server->register(
			'get_convention',
			array( 'id' => 'xsd:int' ),
			array( 'return' => 'tns:convention' ),
			'conventions',
			'conventions#get_convention',
			'rpc',
			'encoded',
			'Get a Convention by ID' );

	// Get All Conventions. Input parameter is ignored.
	$server->register(
			'get_all_conventions',
			array( 'ignore' => 'xsd:int' ),
			array( 'return' => 'tns:convention_array' ),
			'conventions',
			'conventions#get_all_conventions',
			'rpc',
			'encoded',
			'Get all Conventions' );

	// Get All Conventions for a Country.
	$server->register(
			'get_conventions_by_country',
			array( 'country_id' => 'xsd:int' ),
			array( 'return' => 'tns:convention_array' ),
			'conventions',
			'conventions#get_conventions_by_country',
			'rpc',
			'encoded',
			'Get all Conventions for a Country' );

	// Get All Conventions for a Continent.
	$server->register(
			'get_conventions_by_continent',
			array( 'continent_id' => 'xsd:int' ),
			array( 'return' => 'tns:convention_array' ),
			'conventions',
			'conventions#get_conventions_by_continent',
			'rpc',
			'encoded',
			'Get all Conventions for a Continent' );

	// Get All Past Conventions. Input parameter is ignored.
	$server->register(
			'get_all_past_conventions',
			array( 'ignore' => 'xsd:int' ),
			array( 'return' => 'tns:convention_array' ),
			'conventions',
			'conventions#get_all_past_conventions',
			'rpc',
			'encoded',
			'Get all past Conventions' );

	// Get All Past Conventions for a Country.
	$server->register(
			'get_past_conventions_by_country',
			array( 'country_id' => 'xsd:int' ),
			array( 'return' => 'tns:convention_array' ),
			'conventions',
			'conventions#get_past_conventions_by_country',
			'rpc',
			'encoded',
			'Get all past Conventions for a Country' );

	// Get All Past Conventions for a Continent.
	$server->register(
			'get_past_conventions_by_continent',
			array( 'continent_id' => 'xsd:int' ),
			array( 'return' => 'tns:convention_array' ),
			'conventions',
			'conventions#get_past_conventions_by_continent',
			'rpc',
			'encoded',
			'Get all past Conventions for a Continent' );

	// Now write the actual functions to do the work...

	function get_continent( $id )
	{
		// Connect to database
		$db_connection = connect_to_database();

		// Query for result
		$sql = 'select * from continent where id = ' . $id;

		$result = mysql_query( $sql, $db_connection );

		if ( $result == NULL )
		{
			return create_soap_error( "Database error" );
		}

		$row = mysql_fetch_array( $result );

		if ( $row == NULL )
		{
			return create_soap_error( "ID not found" );
		}

		// Get result
		$continent = array( 
				'id' => $row[ 'id' ],
				'name' => $row[ 'name' ] );

		// Close DB stuff
		mysql_free_result( $result );
		mysql_close( $db_connection );

		// Return result
		return $continent;
	}

	function get_all_continents( $ignore )
	{
		// Connect to database
		$db_connection = connect_to_database();

		// Query for result
		$sql = 'select * from continent';

		$result = mysql_query( $sql, $db_connection );

		if ( $result == NULL )
		{
			return create_soap_error( "Database error" );
		}

		// Get result
		$row = mysql_fetch_array( $result );

		$continents = array();
		$continent_counter = 0;

		while ( $row != NULL )
		{
			$continent = array( 
					'id' => $row[ 'id' ],
					'name' => $row[ 'name' ] );

			$continents[ $continent_counter ] = $continent;
			$continent_counter++;

			$row = mysql_fetch_array( $result );
		}

		// Close DB stuff
		mysql_free_result( $result );
		mysql_close( $db_connection );

		// Return result
		return $continents;
	}

	function get_country( $id )
	{
		// Connect to database
		$db_connection = connect_to_database();

		// Query for result
		$sql = 'select continent.id as continent_id, continent.name as continent_name, '
			 . 'country.id as id, country.name as name, country.flag_file as flag_file '
			 . 'from continent, country where continent.id = country.continent_id '
			 . 'and country.id = ' . $id;

		$result = mysql_query( $sql, $db_connection );

		if ( $result == NULL )
		{
			return create_soap_error( "Database error" );
		}

		$row = mysql_fetch_array( $result );

		if ( $row == NULL )
		{
			return create_soap_error( "ID not found" );
		}

		// Get result
		$country = array( 
				'id' => $row[ 'id' ],
				'name' => $row[ 'name' ],
				'continent_id' => $row[ 'continent_id' ],
				'continent_name' => $row[ 'continent_name' ],
				'flag' => ( $row[ 'flag_file' ] != NULL ) );

		// Close DB stuff
		mysql_free_result( $result );
		mysql_close( $db_connection );

		// Return result
		return $country;
	}

	function get_all_countries( $ignore )
	{
		// Connect to database
		$db_connection = connect_to_database();

		// Query for result
		$sql = 'select continent.id as continent_id, continent.name as continent_name, '
			 . 'country.id as id, country.name as name, country.flag_file as flag_file '
			 . 'from continent, country where continent.id = country.continent_id';

		$result = mysql_query( $sql, $db_connection );

		if ( $result == NULL )
		{
			return create_soap_error( "Database error" );
		}

		// Get result
		$row = mysql_fetch_array( $result );

		$countries = array();
		$country_counter = 0;
		
		while ( $row != NULL )
		{	
			$country = array( 
					'id' => $row[ 'id' ],
					'name' => $row[ 'name' ],
					'continent_id' => $row[ 'continent_id' ],
					'continent_name' => $row[ 'continent_name' ],
					'flag' => ( $row[ 'flag_file' ] != NULL ) );

			$countries[ $country_counter ] = $country;
			$country_counter++;

			$row = mysql_fetch_array( $result );
		}

		// Close DB stuff
		mysql_free_result( $result );
		mysql_close( $db_connection );

		// Return result
		return $countries;
	}

	function get_convention( $id )
	{
		// Connect to database
		$db_connection = connect_to_database();

		// Query for result
		$sql = 'select continent.id as continent_id, continent.name as continent_name, '
			 . 'country.id as country_id, country.name as country_name, '
			 . 'convention.id, convention.name, '
			 . 'year( convention.start_date ) as start_year, '
			 . 'month( convention.start_date ) as start_month, '
			 . 'monthname( convention.start_date ) as start_month_name, '
			 . 'dayofmonth( convention.start_date ) as start_day, '
			 . 'year( convention.end_date ) as end_year, '
			 . 'month( convention.end_date ) as end_month, '
			 . 'monthname( convention.end_date ) as end_month_name, '
			 . 'dayofmonth( convention.end_date ) as end_day, '
			 . 'convention.location, convention.contact, convention.comments, '
			 . 'convention.email, convention.url '
			 . 'from continent, country, convention where continent.id = country.continent_id '
			 . 'and convention.country_id = country.id and convention.id = ' . $id;

		$result = mysql_query( $sql, $db_connection );

		if ( $result == NULL )
		{
			return create_soap_error( "Database error" );
		}

		$row = mysql_fetch_array( $result );

		if ( $row == NULL )
		{
			return create_soap_error( "ID not found" );
		}

		// Obfuscate the e-mail address
		$row[ 'email' ] = str_replace( "@", " (at) ", $row[ 'email' ] );

		// Get result
		$convention = $row;

		// Close DB stuff
		mysql_free_result( $result );
		mysql_close( $db_connection );

		// Return result
		return $convention;
	}

	function get_all_conventions( $ignore )
	{
		// Connect to database
		$db_connection = connect_to_database();

		// Query for result
		$sql = 'select continent.id as continent_id, continent.name as continent_name, '
			 . 'country.id as country_id, country.name as country_name, '
			 . 'convention.id, convention.name, '
			 . 'year( convention.start_date ) as start_year, '
			 . 'month( convention.start_date ) as start_month, '
			 . 'monthname( convention.start_date ) as start_month_name, '
			 . 'dayofmonth( convention.start_date ) as start_day, '
			 . 'year( convention.end_date ) as end_year, '
			 . 'month( convention.end_date ) as end_month, '
			 . 'monthname( convention.end_date ) as end_month_name, '
			 . 'dayofmonth( convention.end_date ) as end_day, '
			 . 'convention.location, convention.contact, convention.comments, '
			 . 'convention.email, convention.url '
			 . 'from continent, country, convention where continent.id = country.continent_id '
			 . 'and convention.country_id = country.id and convention.end_date > current_date() '
			 . 'order by convention.start_date';

		$result = mysql_query( $sql, $db_connection );

		if ( $result == NULL )
		{
			return create_soap_error( "Database error" );
		}

		// Get result
		$row = mysql_fetch_array( $result );

		$conventions = array();
		$convention_counter = 0;

		while ( $row != NULL )
		{
			// Obfuscate the e-mail address
			$row[ 'email' ] = str_replace( "@", " (at) ", $row[ 'email' ] );

			$conventions[ $convention_counter ] = $row;
			$convention_counter++;

			$row = mysql_fetch_array( $result );
		}

		// Close DB stuff
		mysql_free_result( $result );
		mysql_close( $db_connection );

		// Return result
		return $conventions;
	}

	function get_conventions_by_country( $country_id )
	{
		// Connect to database
		$db_connection = connect_to_database();

		// Query for result
		$sql = 'select continent.id as continent_id, continent.name as continent_name, '
			 . 'country.id as country_id, country.name as country_name, '
			 . 'convention.id, convention.name, '
			 . 'year( convention.start_date ) as start_year, '
			 . 'month( convention.start_date ) as start_month, '
			 . 'monthname( convention.start_date ) as start_month_name, '
			 . 'dayofmonth( convention.start_date ) as start_day, '
			 . 'year( convention.end_date ) as end_year, '
			 . 'month( convention.end_date ) as end_month, '
			 . 'monthname( convention.end_date ) as end_month_name, '
			 . 'dayofmonth( convention.end_date ) as end_day, '
			 . 'convention.location, convention.contact, convention.comments, '
			 . 'convention.email, convention.url '
			 . 'from continent, country, convention where continent.id = country.continent_id '
			 . 'and convention.country_id = country.id and convention.end_date > current_date() '
			 . 'and country_id = ' . $country_id . ' order by convention.start_date';

		$result = mysql_query( $sql, $db_connection );

		if ( $result == NULL )
		{
			return create_soap_error( "Database error" );
		}

		// Get result
		$row = mysql_fetch_array( $result );

		$conventions = array();
		$convention_counter = 0;

		while ( $row != NULL )
		{
			// Obfuscate the e-mail address
			$row[ 'email' ] = str_replace( "@", " (at) ", $row[ 'email' ] );

			$conventions[ $convention_counter ] = $row;
			$convention_counter++;

			$row = mysql_fetch_array( $result );
		}

		// Close DB stuff
		mysql_free_result( $result );
		mysql_close( $db_connection );

		// Return result
		return $conventions;
	}

	function get_conventions_by_continent( $continent_id )
	{
		// Connect to database
		$db_connection = connect_to_database();

		// Query for result
		$sql = 'select continent.id as continent_id, continent.name as continent_name, '
			 . 'country.id as country_id, country.name as country_name, '
			 . 'convention.id, convention.name, '
			 . 'year( convention.start_date ) as start_year, '
			 . 'month( convention.start_date ) as start_month, '
			 . 'monthname( convention.start_date ) as start_month_name, '
			 . 'dayofmonth( convention.start_date ) as start_day, '
			 . 'year( convention.end_date ) as end_year, '
			 . 'month( convention.end_date ) as end_month, '
			 . 'monthname( convention.end_date ) as end_month_name, '
			 . 'dayofmonth( convention.end_date ) as end_day, '
			 . 'convention.location, convention.contact, convention.comments, '
			 . 'convention.email, convention.url '
			 . 'from continent, country, convention where continent.id = country.continent_id '
			 . 'and convention.country_id = country.id and convention.end_date > current_date() '
			 . 'and continent_id = ' . $continent_id . ' order by convention.start_date';

		$result = mysql_query( $sql, $db_connection );

		if ( $result == NULL )
		{
			return create_soap_error( "Database error" );
		}

		// Get result
		$row = mysql_fetch_array( $result );

		$conventions = array();
		$convention_counter = 0;

		while ( $row != NULL )
		{
			// Obfuscate the e-mail address
			$row[ 'email' ] = str_replace( "@", " (at) ", $row[ 'email' ] );

			$conventions[ $convention_counter ] = $row;
			$convention_counter++;

			$row = mysql_fetch_array( $result );
		}

		// Close DB stuff
		mysql_free_result( $result );
		mysql_close( $db_connection );

		// Return result
		return $conventions;
	}

	function get_all_past_conventions( $ignore )
	{
		// Connect to database
		$db_connection = connect_to_database();

		// Query for result
		$sql = 'select continent.id as continent_id, continent.name as continent_name, '
			 . 'country.id as country_id, country.name as country_name, '
			 . 'convention.id, convention.name, '
			 . 'year( convention.start_date ) as start_year, '
			 . 'month( convention.start_date ) as start_month, '
			 . 'monthname( convention.start_date ) as start_month_name, '
			 . 'dayofmonth( convention.start_date ) as start_day, '
			 . 'year( convention.end_date ) as end_year, '
			 . 'month( convention.end_date ) as end_month, '
			 . 'monthname( convention.end_date ) as end_month_name, '
			 . 'dayofmonth( convention.end_date ) as end_day, '
			 . 'convention.location, convention.contact, convention.comments, '
			 . 'convention.email, convention.url '
			 . 'from continent, country, convention where continent.id = country.continent_id '
			 . 'and convention.country_id = country.id and convention.end_date <= current_date() '
			 . 'order by convention.start_date';

		$result = mysql_query( $sql, $db_connection );

		if ( $result == NULL )
		{
			return create_soap_error( "Database error" );
		}

		// Get result
		$row = mysql_fetch_array( $result );

		$conventions = array();
		$convention_counter = 0;

		while ( $row != NULL )
		{
			// Obfuscate the e-mail address
			$row[ 'email' ] = str_replace( "@", " (at) ", $row[ 'email' ] );

			$conventions[ $convention_counter ] = $row;
			$convention_counter++;

			$row = mysql_fetch_array( $result );
		}

		// Close DB stuff
		mysql_free_result( $result );
		mysql_close( $db_connection );

		// Return result
		return $conventions;
	}

	function get_past_conventions_by_country( $country_id )
	{
		// Connect to database
		$db_connection = connect_to_database();

		// Query for result
		$sql = 'select continent.id as continent_id, continent.name as continent_name, '
			 . 'country.id as country_id, country.name as country_name, '
			 . 'convention.id, convention.name, '
			 . 'year( convention.start_date ) as start_year, '
			 . 'month( convention.start_date ) as start_month, '
			 . 'monthname( convention.start_date ) as start_month_name, '
			 . 'dayofmonth( convention.start_date ) as start_day, '
			 . 'year( convention.end_date ) as end_year, '
			 . 'month( convention.end_date ) as end_month, '
			 . 'monthname( convention.end_date ) as end_month_name, '
			 . 'dayofmonth( convention.end_date ) as end_day, '
			 . 'convention.location, convention.contact, convention.comments, '
			 . 'convention.email, convention.url '
			 . 'from continent, country, convention where continent.id = country.continent_id '
			 . 'and convention.country_id = country.id and convention.end_date <= current_date() '
			 . 'and country_id = ' . $country_id . ' order by convention.start_date';

		$result = mysql_query( $sql, $db_connection );

		if ( $result == NULL )
		{
			return create_soap_error( "Database error" );
		}

		// Get result
		$row = mysql_fetch_array( $result );

		$conventions = array();
		$convention_counter = 0;

		while ( $row != NULL )
		{
			// Obfuscate the e-mail address
			$row[ 'email' ] = str_replace( "@", " (at) ", $row[ 'email' ] );

			$conventions[ $convention_counter ] = $row;
			$convention_counter++;

			$row = mysql_fetch_array( $result );
		}

		// Close DB stuff
		mysql_free_result( $result );
		mysql_close( $db_connection );

		// Return result
		return $conventions;
	}

	function get_past_conventions_by_continent( $continent_id )
	{
		// Connect to database
		$db_connection = connect_to_database();

		// Query for result
		$sql = 'select continent.id as continent_id, continent.name as continent_name, '
			 . 'country.id as country_id, country.name as country_name, '
			 . 'convention.id, convention.name, '
			 . 'year( convention.start_date ) as start_year, '
			 . 'month( convention.start_date ) as start_month, '
			 . 'monthname( convention.start_date ) as start_month_name, '
			 . 'dayofmonth( convention.start_date ) as start_day, '
			 . 'year( convention.end_date ) as end_year, '
			 . 'month( convention.end_date ) as end_month, '
			 . 'monthname( convention.end_date ) as end_month_name, '
			 . 'dayofmonth( convention.end_date ) as end_day, '
			 . 'convention.location, convention.contact, convention.comments, '
			 . 'convention.email, convention.url '
			 . 'from continent, country, convention where continent.id = country.continent_id '
			 . 'and convention.country_id = country.id and convention.end_date <= current_date() '
			 . 'and continent_id = ' . $continent_id . ' order by convention.start_date';

		$result = mysql_query( $sql, $db_connection );

		if ( $result == NULL )
		{
			return create_soap_error( "Database error" );
		}

		// Get result
		$row = mysql_fetch_array( $result );

		$conventions = array();
		$convention_counter = 0;

		while ( $row != NULL )
		{
			// Obfuscate the e-mail address
			$row[ 'email' ] = str_replace( "@", " (at) ", $row[ 'email' ] );

			$conventions[ $convention_counter ] = $row;
			$convention_counter++;

			$row = mysql_fetch_array( $result );
		}

		// Close DB stuff
		mysql_free_result( $result );
		mysql_close( $db_connection );

		// Return result
		return $conventions;
	}

	function create_soap_error( $error_text )
	{
		return new soap_fault( 'SERVER', '', $error_text, '' );
	}

	// Use the request to (try to) invoke the service

	$HTTP_RAW_POST_DATA = isset($HTTP_RAW_POST_DATA) ? $HTTP_RAW_POST_DATA : '';
	$server->service($HTTP_RAW_POST_DATA);

?>
