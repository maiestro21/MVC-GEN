<?php
class @@controller_name_capitalize@@_model extends CI_Model
{


    function add($data)
    {
        $this->db->insert('@@controller_name@@', $data);
        return $this->db->insert_id();
    }

    function get_all()
    {
        $result = $this->db->get('@@controller_name@@');
        return $result->result();
    }


    function get_by_id($id){
        $this->db->where("@@id_field@@", $id);
        $result = $this->db->get('@@controller_name@@');
        return $result->result();

    }


    function update($id, $data){
        $this->db->where('@@id_field@@',$id);
        $this->db->update('@@controller_name@@',$data);
        return $this->db->affected_rows();
    }



    function delete($id){
        $this->db->where('@@id_field@@', $id);
        $this->db->delete('@@controller_name@@');
        return $this->db->affected_rows();
    }
}
