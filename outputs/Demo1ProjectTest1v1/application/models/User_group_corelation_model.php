<?php
class User_group_corelation_model extends CI_Model
{


    function add($data)
    {
        $this->db->insert('user_group_corelation', $data);
        return $this->db->insert_id();
    }

    function get_all()
    {
        $result = $this->db->get('user_group_corelation');
        return $result->result();
    }


    function get_by_id($id){
        $this->db->where("id_user_group_corelation", $id);
        $result = $this->db->get('user_group_corelation');
        return $result->result();

    }


    function update($id, $data){
        $this->db->where('id_user_group_corelation',$id);
        $this->db->update('user_group_corelation',$data);
        return $this->db->affected_rows();
    }



    function delete($id){
        $this->db->where('id_user_group_corelation', $id);
        $this->db->delete('user_group_corelation');
        return $this->db->affected_rows();
    }
}
