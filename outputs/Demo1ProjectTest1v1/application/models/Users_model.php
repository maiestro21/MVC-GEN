<?php
class Users_model extends CI_Model
{


    function add($data)
    {
        $this->db->insert('users', $data);
        return $this->db->insert_id();
    }

    function get_all()
    {
        $result = $this->db->get('users');
        return $result->result();
    }


    function get_by_id($id){
        $this->db->where("id_users", $id);
        $result = $this->db->get('users');
        return $result->result();

    }


    function update($id, $data){
        $this->db->where('id_users',$id);
        $this->db->update('users',$data);
        return $this->db->affected_rows();
    }



    function delete($id){
        $this->db->where('id_users', $id);
        $this->db->delete('users');
        return $this->db->affected_rows();
    }
}
