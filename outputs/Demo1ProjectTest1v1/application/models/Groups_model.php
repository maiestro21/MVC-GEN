<?php
class Groups_model extends CI_Model
{


    function add($data)
    {
        $this->db->insert('groups', $data);
        return $this->db->insert_id();
    }

    function get_all()
    {
        $result = $this->db->get('groups');
        return $result->result();
    }


    function get_by_id($id){
        $this->db->where("id_groups", $id);
        $result = $this->db->get('groups');
        return $result->result();

    }


    function update($id, $data){
        $this->db->where('id_groups',$id);
        $this->db->update('groups',$data);
        return $this->db->affected_rows();
    }



    function delete($id){
        $this->db->where('id_groups', $id);
        $this->db->delete('groups');
        return $this->db->affected_rows();
    }
}
