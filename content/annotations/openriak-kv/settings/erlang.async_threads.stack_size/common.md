# Description

Suggested stack size for each asynchronous driver thread, translated by the schema into the VM's stack-size units. Larger stacks consume more memory across the pool; platforms may ignore the suggestion.

# Constraints

- Size must be a multiple of the system's Word Size in bytes. Use a size from (16 × 1024 × Word Size) to (8,192 × 1024 × Word Size) bytes. Word Size is usually 4 bytes on 32-bit systems and 8 bytes on 64-bit systems. In the Linux shell, `getconf LONG_BIT` reports the system's word size in bits; divide by 8 to get bytes.

# Notes

The [schema checks](https://github.com/OpenRiak/cuttlefish/blob/3d66fbdc6f1fe4fa551a86b25d28e8eb31e34122/priv/erlang_vm.schema#L140) use the Erlang runtime's external word size. The range above corresponds to 64 KB–32 MB for a 4-byte word or 128 KB–64 MB for an 8-byte word. The range check and VM conversion round down to whole kilowords (1,024 words), so a word-aligned remainder smaller than one kiloword is discarded, including just above the stated upper bound. For an Erlang build whose word size differs from the host, the runtime's word size is authoritative.

# Tags

feature: erlang-runtime
repository: cuttlefish
module: erlang_vm.schema
concept: concurrency, runtime

# Reviewed against

3.4.0: f762b169d98c0e84ed648a38e52244a57e6969b61fc4c3988dc00188bb2f8a4e
3.4.1: f762b169d98c0e84ed648a38e52244a57e6969b61fc4c3988dc00188bb2f8a4e
