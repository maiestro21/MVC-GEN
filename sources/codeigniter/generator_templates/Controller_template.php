<?php
defined('BASEPATH') OR exit('No direct script access allowed');


class @@controller_name_capitalize@@ extends CI_Controller {

	function __construct(){
		parent::__construct();
		$this->load->model('@@controller_name@@_model');
	}

	public function index()
	{
		$this->load->view('@@view_name@@');
	}
	
	//GET ALL
	public function get_all(){
		header('Content-Type: application/json');
		if ($this->input->server('REQUEST_METHOD') === 'GET') {
			$data = $this->@@controller_name@@_model->get_all();
			echo json_encode($data);
		 } else{
			echo json_encode(array("error"=>"Invalid method for path."));
		 }

	

	}

	//GET BY ID
	public function get($id){
		header('Content-Type: application/json');
		if ($this->input->server('REQUEST_METHOD') === 'GET') {
			$data = $this->@@controller_name@@_model->get_by_id($id);
			echo json_encode($data);	
		} else {
			echo json_encode(array("error"=>"Invalid method for path."));
		}

	}
	
	//POST
	public function add(){
		header('Content-Type: application/json');
		if ($this->input->server('REQUEST_METHOD') === 'POST') {

			$post_data = $this->input->post();
			$data = array(
				'id' =>$this->@@controller_name@@_model->add($post_data)
			);
			echo json_encode($data);
		} else {
			echo json_encode(array("error"=>"Invalid method for path."));
		}	
	}

	
	
	//PUT
	public function update($id){
		header('Content-Type: application/json');
		if ($this->input->server('REQUEST_METHOD') === 'PUT') {
			$raw_data = file_get_contents('php://input');
			$boundary = substr($raw_data, 0, strpos($raw_data, "\r\n"));
			$parts = array_slice(explode($boundary, $raw_data), 1);
			$data = array();
			foreach ($parts as $part) {
				// If this is the last part, break
				if ($part == "--\r\n") break; 

				// Separate content from headers
				$part = ltrim($part, "\r\n");
				list($raw_headers, $body) = explode("\r\n\r\n", $part, 2);

				// Parse the headers list
				$raw_headers = explode("\r\n", $raw_headers);
				$headers = array();
				foreach ($raw_headers as $header) {
					list($name, $value) = explode(':', $header);
					$headers[strtolower($name)] = ltrim($value, ' '); 
				} 

				// Parse the Content-Disposition
				if (isset($headers['content-disposition'])) {
					$filename = null;
					preg_match(
						'/^(.+); *name="([^"]+)"(; *filename="([^"]+)")?/', 
						$headers['content-disposition'], 
						$matches
					);
					list(, $type, $name) = $matches;
					isset($matches[4]) and $filename = $matches[4]; 

					switch ($name) {
						case 'userfile':
							file_put_contents($filename, $body);
							break;

						default: 
							$data[$name] = substr($body, 0, strlen($body) - 2);
							break;
					} 
				}

			}
			
			$return = array(
				'affected_rows' =>$this->@@controller_name@@_model->update($id, $data)
			);
			echo json_encode($return);
		} else {
			echo json_encode(array("error"=>"Invalid method for path."));
		}	
	}
	
	//DELETE
	public function delete($id){
		header('Content-Type: application/json');
		if ($this->input->server('REQUEST_METHOD') === 'DELETE') {
			
			$return = array(
				'affected_rows' =>$this->@@controller_name@@_model->delete($id)
			);
			echo json_encode($return);
		} else {
			echo json_encode(array("error"=>"Invalid method for path."));
		}	
}
	
}
