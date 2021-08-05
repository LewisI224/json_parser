terraform {
  required_providers {
    libvirt = {
       source = "dmacvicar/libvirt"
    }
  }
}

provider "libvirt" {
  uri = "qemu:///system"
}

resource "libvirt_volume" "$OS$-qcow2" {
  name = "$OS$.qcow2"
  pool = "default"
  source = "$IMAGE$"
  format = "qcow2"
}

data "template_file" "user_data" {
  template = "${file("${path.module}/cloud_init.cfg")}"
}
#Use CloudInit to add the instance
resource "libvirt_cloudinit_disk" "commoninit" {
  name = "commoninit.iso"
  user_data      = "${data.template_file.user_data.rendered}"
}

# Define KVM domain to create
resource "libvirt_domain" "db1" {
  name   = "db1"
  memory = "$RAM$"
  vcpu   = $CPU$

  network_interface {
    network_name = "default"
  }

  disk {
    volume_id = "${libvirt_volume.$OS$-qcow2.id}"
  }

  cloudinit = "${libvirt_cloudinit_disk.commoninit.id}"

  console {
    type = "pty"
    target_type = "serial"
    target_port = "0"
  }

  graphics {
    type = "spice"
    listen_type = "address"
    autoport = true
  }
}