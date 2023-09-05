#include <linux/module.h>
#define INCLUDE_VERMAGIC
#include <linux/build-salt.h>
#include <linux/elfnote-lto.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

BUILD_SALT;
BUILD_LTO_INFO;

MODULE_INFO(vermagic, VERMAGIC_STRING);
MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(".gnu.linkonce.this_module") = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

MODULE_INFO(intree, "Y");

#ifdef CONFIG_RETPOLINE
MODULE_INFO(retpoline, "Y");
#endif

static const struct modversion_info ____versions[]
__used __section("__versions") = {
	{ 0x58c57fee, "module_layout" },
	{ 0xb9681621, "xdp_do_flush" },
	{ 0x2d3385d3, "system_wq" },
	{ 0x60443957, "mdio45_probe" },
	{ 0xf9480c22, "netdev_info" },
	{ 0x8c1b1303, "kmalloc_caches" },
	{ 0xeb233a45, "__kmalloc" },
	{ 0x3059b717, "xsk_tx_release" },
	{ 0x389bc87a, "ethtool_op_get_ts_info" },
	{ 0xc4f0da12, "ktime_get_with_offset" },
	{ 0xf9a482f9, "msleep" },
	{ 0x862258db, "timecounter_init" },
	{ 0x65024c6e, "dcb_ieee_setapp" },
	{ 0xf90a1e85, "__x86_indirect_thunk_r8" },
	{ 0xc5879607, "skb_clone_tx_timestamp" },
	{ 0x9703a412, "pci_enable_sriov" },
	{ 0x619cb7dd, "simple_read_from_buffer" },
	{ 0x89c3b4ae, "pci_write_config_word" },
	{ 0x1b71bf88, "debugfs_create_dir" },
	{ 0xd6ee688f, "vmalloc" },
	{ 0xd327ea61, "param_ops_int" },
	{ 0x4d686820, "dcb_ieee_delapp" },
	{ 0xbce234e6, "napi_disable" },
	{ 0x754d539c, "strlen" },
	{ 0x55eec650, "pci_sriov_set_totalvfs" },
	{ 0x54b1fac6, "__ubsan_handle_load_invalid_value" },
	{ 0xdeddd93e, "napi_consume_skb" },
	{ 0xe45134a9, "napi_schedule_prep" },
	{ 0xd35d23a2, "__napi_schedule_irqoff" },
	{ 0xa5875396, "xdp_master_redirect" },
	{ 0x4e393fae, "seq_open" },
	{ 0x59e5272f, "dma_set_mask" },
	{ 0x43c351d8, "dev_uc_add" },
	{ 0x7c33b76c, "xdp_rxq_info_reg" },
	{ 0x54c8161b, "xp_free" },
	{ 0x8a96008a, "pci_disable_device" },
	{ 0xc7a4fbed, "rtnl_lock" },
	{ 0x92e1ffc, "pci_disable_msix" },
	{ 0x9175eda4, "__mdiobus_register" },
	{ 0x6f8f674a, "bpf_dispatcher_xdp_func" },
	{ 0x4ea25709, "dql_reset" },
	{ 0x3d3defcb, "netdev_set_num_tc" },
	{ 0xf92f03d5, "netif_carrier_on" },
	{ 0xc3c1bed5, "pci_disable_sriov" },
	{ 0x428f67c7, "__hw_addr_sync_dev" },
	{ 0xe0112fc4, "__x86_indirect_thunk_r9" },
	{ 0x2d3c6c65, "seq_printf" },
	{ 0xd559cf5f, "netif_carrier_off" },
	{ 0x56470118, "__warn_printk" },
	{ 0x3c12dfe, "cancel_work_sync" },
	{ 0xb43f9365, "ktime_get" },
	{ 0x74a6cd0, "pci_dev_get" },
	{ 0xc686c0a1, "mdiobus_write" },
	{ 0x66cca4f9, "__x86_indirect_thunk_rcx" },
	{ 0xdaceb7a6, "mdio_mii_ioctl" },
	{ 0x6ea2f113, "xdp_rxq_info_unreg" },
	{ 0xa382fde6, "xp_set_rxq_info" },
	{ 0x664a3230, "pcie_print_link_status" },
	{ 0xfefb9d54, "driver_for_each_device" },
	{ 0x608b0576, "__dev_kfree_skb_any" },
	{ 0xeae3dfd6, "__const_udelay" },
	{ 0xc6f46339, "init_timer_key" },
	{ 0x2d5f69b3, "rcu_read_unlock_strict" },
	{ 0x999e8297, "vfree" },
	{ 0x86007786, "dma_free_attrs" },
	{ 0x5317dd51, "netdev_reset_tc" },
	{ 0xbaf22757, "kvfree_call_rcu" },
	{ 0xb61f07fa, "xsk_set_tx_need_wakeup" },
	{ 0xa94b5a31, "debugfs_create_file" },
	{ 0x44aaf30f, "tsc_khz" },
	{ 0x4629334c, "__preempt_count" },
	{ 0x7a2af7b4, "cpu_number" },
	{ 0xa648e561, "__ubsan_handle_shift_out_of_bounds" },
	{ 0x92eebe42, "netdev_bind_sb_channel_queue" },
	{ 0x97651e6c, "vmemmap_base" },
	{ 0x922f45a6, "__bitmap_clear" },
	{ 0x3559be9e, "ipv6_find_hdr" },
	{ 0x146cc88f, "bpf_master_redirect_enabled_key" },
	{ 0x3c3ff9fd, "sprintf" },
	{ 0x1508c6d0, "mdiobus_unregister" },
	{ 0xab40c0be, "__page_frag_cache_drain" },
	{ 0xbe49f9ed, "seq_read" },
	{ 0x65b95d9a, "pv_ops" },
	{ 0x1a366961, "netdev_walk_all_upper_dev_rcu" },
	{ 0x5c92ee4b, "dma_set_coherent_mask" },
	{ 0x6d370855, "netdev_unbind_sb_channel" },
	{ 0x15ba50a6, "jiffies" },
	{ 0xf9b5d1ac, "__dynamic_netdev_dbg" },
	{ 0xcffc96e, "devm_mdiobus_alloc_size" },
	{ 0xfb384d37, "kasprintf" },
	{ 0xee5d82e4, "xp_dma_unmap" },
	{ 0xb1ce4187, "ptp_clock_unregister" },
	{ 0x6b10bee1, "_copy_to_user" },
	{ 0xf7bd848d, "netdev_set_tc_queue" },
	{ 0xb235d85c, "PDE_DATA" },
	{ 0x17de3d5, "nr_cpu_ids" },
	{ 0x5b8239ca, "__x86_return_thunk" },
	{ 0xbf5014e2, "pci_set_master" },
	{ 0x58b91161, "dca3_get_tag" },
	{ 0x62c0aae7, "__alloc_pages" },
	{ 0xbc66df94, "netif_schedule_queue" },
	{ 0x18e6ab5c, "ptp_clock_event" },
	{ 0x97934ecf, "del_timer_sync" },
	{ 0x2688ec10, "bitmap_zalloc" },
	{ 0x31549b2a, "__x86_indirect_thunk_r10" },
	{ 0x3fe79b2b, "_dev_warn" },
	{ 0xfb578fc5, "memset" },
	{ 0x5338184f, "ethtool_sprintf" },
	{ 0x1b9d8001, "devm_hwmon_device_register_with_groups" },
	{ 0xc5a46eb3, "dcb_getapp" },
	{ 0x3afe4c86, "pci_enable_pcie_error_reporting" },
	{ 0x1a49d664, "dma_sync_single_for_cpu" },
	{ 0xac34ecec, "dca_register_notify" },
	{ 0x1e1e140e, "ns_to_timespec64" },
	{ 0xdc9e923, "proc_mkdir" },
	{ 0xa147e39, "netdev_set_sb_channel" },
	{ 0xc87b3cea, "netif_tx_wake_queue" },
	{ 0x256486f5, "pci_restore_state" },
	{ 0xf8853367, "netif_tx_stop_all_queues" },
	{ 0x1a33ab9, "dca_unregister_notify" },
	{ 0xd35cce70, "_raw_spin_unlock_irqrestore" },
	{ 0x676d1dec, "dev_addr_del" },
	{ 0x84678725, "__SCK__tp_func_xdp_exception" },
	{ 0xc47411c2, "netif_set_xps_queue" },
	{ 0x60bdb375, "eth_platform_get_mac_address" },
	{ 0xcea13561, "ethtool_op_get_link" },
	{ 0xbcab6ee6, "sscanf" },
	{ 0x3c3fce39, "__local_bh_enable_ip" },
	{ 0x449ad0a7, "memcmp" },
	{ 0x5a5a2271, "__cpu_online_mask" },
	{ 0xa50a3da7, "_find_next_bit" },
	{ 0x9ec6ca96, "ktime_get_real_ts64" },
	{ 0xde80cd09, "ioremap" },
	{ 0xa00aca2a, "dql_completed" },
	{ 0x4c9d28b0, "phys_base" },
	{ 0xcd279169, "nla_find" },
	{ 0xd61eeee, "__bitmap_subset" },
	{ 0xfbb597c8, "xsk_get_pool_from_qid" },
	{ 0x92d9c6f1, "free_netdev" },
	{ 0x1a79c8e9, "__x86_indirect_thunk_r13" },
	{ 0x6a429d73, "mdiobus_read" },
	{ 0xcaea09ef, "register_netdev" },
	{ 0x1f629695, "xsk_uses_need_wakeup" },
	{ 0xe5428e75, "xsk_clear_rx_need_wakeup" },
	{ 0x5a921311, "strncmp" },
	{ 0xfc7c1baf, "napi_enable" },
	{ 0xff0ec5c, "pci_read_config_word" },
	{ 0xc11f202d, "pcie_flr" },
	{ 0x2e67402e, "debugfs_remove" },
	{ 0x699329e0, "dma_alloc_attrs" },
	{ 0xcfd6a384, "pci_get_domain_bus_and_slot" },
	{ 0x8c03d20c, "destroy_workqueue" },
	{ 0x8885fb5d, "kfree_skb_reason" },
	{ 0xa8647e70, "netif_set_real_num_rx_queues" },
	{ 0xc38c83b8, "mod_timer" },
	{ 0x5112428c, "netif_set_real_num_tx_queues" },
	{ 0xea6f0d07, "netif_napi_add" },
	{ 0x55385e2e, "__x86_indirect_thunk_r14" },
	{ 0x77b83383, "xsk_tx_peek_desc" },
	{ 0xabe2f285, "dcb_ieee_getapp_mask" },
	{ 0xa63c088, "xp_dma_sync_for_cpu_slow" },
	{ 0x3e796112, "ptp_clock_register" },
	{ 0x92d5838e, "request_threaded_irq" },
	{ 0xfa65760d, "xdp_return_frame" },
	{ 0x5b4aad3a, "dca_add_requester" },
	{ 0x6091797f, "synchronize_rcu" },
	{ 0x245919b4, "simple_open" },
	{ 0x1312879b, "softnet_data" },
	{ 0x10c626cf, "_dev_err" },
	{ 0xee53d911, "pci_enable_msi" },
	{ 0xf84bd6ee, "bpf_stats_enabled_key" },
	{ 0xc8a91f5b, "cpumask_local_spread" },
	{ 0xe523ad75, "synchronize_irq" },
	{ 0x6f9e763b, "timecounter_read" },
	{ 0xbe5c6e1d, "build_skb" },
	{ 0x800473f, "__cond_resched" },
	{ 0xfa7526bd, "flow_block_cb_setup_simple" },
	{ 0x34c810c2, "device_wakeup_disable" },
	{ 0x7cd8d75e, "page_offset_base" },
	{ 0xad549937, "eth_get_headlen" },
	{ 0x72d75ae5, "xp_raw_get_dma" },
	{ 0x87a21cb3, "__ubsan_handle_out_of_bounds" },
	{ 0x167c5967, "print_hex_dump" },
	{ 0xfacef123, "pci_select_bars" },
	{ 0xbc3f2cb0, "timecounter_cyc2time" },
	{ 0x65541ac5, "netif_device_attach" },
	{ 0xd3a5f48e, "napi_gro_receive" },
	{ 0x1cdd8065, "_dev_info" },
	{ 0x39fe7c15, "__hw_addr_unsync_dev" },
	{ 0x23622b7a, "dev_addr_add" },
	{ 0x82a3c1be, "__free_pages" },
	{ 0x6383b27c, "__x86_indirect_thunk_rdx" },
	{ 0x618911fc, "numa_node" },
	{ 0xa92088e3, "netif_device_detach" },
	{ 0xe40adf30, "__alloc_skb" },
	{ 0xa916b694, "strnlen" },
	{ 0x4e529b97, "xsk_set_rx_need_wakeup" },
	{ 0x648ae63d, "pci_enable_msix_range" },
	{ 0x296695f, "refcount_warn_saturate" },
	{ 0xd0da656b, "__stack_chk_fail" },
	{ 0xc01648cd, "skb_checksum_help" },
	{ 0xe6d2458e, "do_trace_netlink_extack" },
	{ 0xfadb3e5e, "ndo_dflt_fdb_add" },
	{ 0x92997ed8, "_printk" },
	{ 0x7d476565, "napi_complete_done" },
	{ 0x6b8b3720, "dma_map_page_attrs" },
	{ 0x65487097, "__x86_indirect_thunk_rax" },
	{ 0x7a43f336, "pci_read_config_dword" },
	{ 0xfc0ebd13, "eth_type_trans" },
	{ 0x3a26ed11, "sched_clock" },
	{ 0xe787b2ef, "xdp_rxq_info_reg_mem_model" },
	{ 0xc713308c, "dev_driver_string" },
	{ 0xa90363c4, "pskb_expand_head" },
	{ 0xbdfb6dbb, "__fentry__" },
	{ 0xa2c90c0f, "netdev_err" },
	{ 0x467df16d, "netdev_rss_key_fill" },
	{ 0xcbd4898c, "fortify_panic" },
	{ 0x159ca228, "pci_unregister_driver" },
	{ 0xb5e498bb, "kmem_cache_alloc_trace" },
	{ 0xba8fbd64, "_raw_spin_lock" },
	{ 0xb19a5453, "__per_cpu_offset" },
	{ 0xca21ebd3, "bitmap_free" },
	{ 0x34db050b, "_raw_spin_lock_irqsave" },
	{ 0x236364b6, "__netif_napi_del" },
	{ 0x6d397268, "xdp_rxq_info_unreg_mem_model" },
	{ 0xd60974d1, "pci_set_power_state" },
	{ 0xf428c545, "udp_tunnel_nic_ops" },
	{ 0x5e7cac88, "remove_proc_subtree" },
	{ 0x756b95f1, "netdev_warn" },
	{ 0xc3055d20, "usleep_range_state" },
	{ 0x31011ca2, "proc_create_data" },
	{ 0xbb4f4766, "simple_write_to_buffer" },
	{ 0xbe7287ca, "eth_validate_addr" },
	{ 0xe80ad1ff, "pci_disable_pcie_error_reporting" },
	{ 0x774b8101, "xdp_do_redirect" },
	{ 0xbe1dc92, "seq_lseek" },
	{ 0x37a0cba, "kfree" },
	{ 0x69acdf38, "memcpy" },
	{ 0x199ef5bc, "___pskb_trim" },
	{ 0x15b80c0c, "ptp_clock_index" },
	{ 0xb7bf99a0, "pci_disable_msi" },
	{ 0xe6be92f9, "dev_trans_start" },
	{ 0x7b37d4a7, "_find_first_zero_bit" },
	{ 0x4655d89f, "skb_add_rx_frag" },
	{ 0xe540d110, "pci_num_vf" },
	{ 0xedc03953, "iounmap" },
	{ 0xdbf04499, "dma_sync_single_for_device" },
	{ 0x6cba7b15, "__pci_register_driver" },
	{ 0x15af7f4, "system_state" },
	{ 0x53569707, "this_cpu_off" },
	{ 0xb97d4e91, "dma_unmap_page_attrs" },
	{ 0xfbc440b0, "pci_get_device" },
	{ 0x63c4d61f, "__bitmap_weight" },
	{ 0x79c3911d, "xdp_convert_zc_to_xdp_frame" },
	{ 0x1a9e375d, "unregister_netdev" },
	{ 0xcd1d7daa, "ndo_dflt_bridge_getlink" },
	{ 0x5c2bcd37, "bpf_warn_invalid_xdp_action" },
	{ 0x1ba59527, "__kmalloc_node" },
	{ 0x9564c1a, "pci_dev_put" },
	{ 0xc5b6f236, "queue_work_on" },
	{ 0x53894ae9, "pci_vfs_assigned" },
	{ 0x656e4a6e, "snprintf" },
	{ 0x16347df3, "seq_release" },
	{ 0xbb7195a5, "xdp_warn" },
	{ 0xe113bbbc, "csum_partial" },
	{ 0xaca48ad3, "consume_skb" },
	{ 0xbdac619e, "dca_remove_requester" },
	{ 0xb2240e8b, "pci_enable_device_mem" },
	{ 0x9bde7ca1, "__napi_alloc_skb" },
	{ 0xc60d0620, "__num_online_cpus" },
	{ 0x748728db, "skb_tstamp_tx" },
	{ 0x46b3a3c, "skb_put" },
	{ 0xb345d48, "pci_wake_from_d3" },
	{ 0xde81d527, "devm_kmalloc" },
	{ 0x68b0002a, "pci_release_selected_regions" },
	{ 0xc5e8ddf4, "pci_request_selected_regions" },
	{ 0x59c6aff4, "irq_set_affinity_hint" },
	{ 0x13c49cc2, "_copy_from_user" },
	{ 0x24ab45ad, "param_ops_uint" },
	{ 0x9739afb4, "skb_copy_bits" },
	{ 0xa1a65bcd, "xp_dma_map" },
	{ 0x49cd25ed, "alloc_workqueue" },
	{ 0x69ff9a3e, "bpf_prog_put" },
	{ 0x619a3b7e, "pci_find_ext_capability" },
	{ 0x23fd3028, "vmalloc_node" },
	{ 0x6e720ff2, "rtnl_unlock" },
	{ 0x9e7d6bd0, "__udelay" },
	{ 0x8156be53, "__skb_pad" },
	{ 0x4ee69c63, "pcie_capability_read_word" },
	{ 0x727d0344, "device_set_wakeup_enable" },
	{ 0x8fa9d9e8, "__SCT__tp_func_xdp_exception" },
	{ 0xcdff2674, "dev_get_stats" },
	{ 0xf7bae77c, "xp_alloc" },
	{ 0xc31db0ce, "is_vmalloc_addr" },
	{ 0xc1514a3b, "free_irq" },
	{ 0x817b198f, "xp_dma_sync_for_device_slow" },
	{ 0xaf59f5e2, "pci_save_state" },
	{ 0x61f316ab, "alloc_etherdev_mqs" },
	{ 0xccbb5a70, "xsk_tx_completed" },
	{ 0x9f223fe4, "__tracepoint_xdp_exception" },
	{ 0x8966f63d, "netdev_crit" },
};

MODULE_INFO(depends, "mdio,dca");

MODULE_ALIAS("pci:v00008086d000010B6sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000010C6sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000010C7sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000010C8sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d0000150Bsv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000010DDsv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000010ECsv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000010F1sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000010E1sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000010F4sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000010DBsv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00001508sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000010F7sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000010FCsv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00001517sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000010FBsv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00001507sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00001514sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000010F9sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d0000152Asv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00001529sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d0000151Csv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000010F8sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00001528sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d0000154Dsv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d0000154Fsv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00001558sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00001557sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d0000154Asv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00001560sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d00001563sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000015D1sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000015AAsv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000015B0sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000015ABsv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000015ADsv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000015ACsv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000015AEsv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000015C2sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000015C3sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000015C4sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000015C6sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000015C7sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000015C8sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000015CEsv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000015E4sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00008086d000015E5sv*sd*bc*sc*i*");

MODULE_INFO(srcversion, "F112D94FA3B518932BF7407");
