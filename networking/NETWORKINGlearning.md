# Networking Notes 

## Table of contents
1. [Introduction](#introduction)
2. [Why networking matters in DevOps](#why-networking-matters-in-devops)
3. [LAN vs WAN](#lan-vs-wan)
4. [Networking devices](#networking-devices)
5. [IP addresses and MAC addresses](#ip-addresses-and-mac-addresses)
6. [Ports and protocols](#ports-and-protocols)
7. [TCP vs UDP](#tcp-vs-udp)
8. [OSI model](#osi-model)
9. [TCP IP model](#tcp-ip-model)
10. [OSI example sender and receiver](#osi-example-sender-and-receiver)
11. [DNS fundamentals](#dns-fundamentals)
12. [DNS records](#dns-records)
13. [DNS hierarchy and resolution](#dns-hierarchy-and-resolution)
14. [DNS tools](#dns-tools)
15. [The hosts file](#the-hosts-file)
16. [Routing](#routing)
17. [Subnetting and CIDR](#subnetting-and-cidr)
18. [NAT](#nat)
19. [Network troubleshooting](#network-troubleshooting)
20. [Cloud native networking](#cloud-native-networking)

---

## Introduction

A computer network is simply **connected devices sharing information**.

In DevOps, networking shows up everywhere:
- apps talking to services
- servers talking to databases
- CI/CD pipelines talking to cloud APIs
- load balancers, DNS, TLS, routing, and firewalls

---

## Why networking matters in DevOps

| Area | Why it matters |
| --- | --- |
| Server interaction | Enables communication between servers and applications |
| Deployment | Critical for launching and updating applications reliably |
| Management | Crucial for monitoring and managing infrastructure |
| Optimisation | Helps troubleshooting, performance, and scalability |

---

## LAN vs WAN

| Type | What it is | Example |
| --- | --- | --- |
| LAN (Local Area Network) | Small area network connecting nearby devices | Home Wi-Fi, office network |
| WAN (Wide Area Network) | Large area network connecting multiple LANs | The internet |

---

## Networking devices

| Device | What it does |
| --- | --- |
| Switch | Connects devices in the same network (LAN), manages data flow within the local network |
| Router | Directs traffic between networks, connects different networks together |
| Firewall | Protects networks from unauthorised access by monitoring and controlling incoming and outgoing traffic |

---

## IP addresses and MAC addresses

### IP addresses
An IP address is a **unique identifier** for a device on a network.

| Type | Format | Notes |
| --- | --- | --- |
| IPv4 | `192.168.0.5` | 32-bit address |
| IPv6 | `2001:0db8:85a3:0000:0000:8a2e:0370:7334` | 128-bit address, written as eight groups of hexadecimal |

### MAC addresses
A MAC address is a **unique identifier** assigned to a network interface.

- Example: `00:1A:2B:3C:4D:5E`
- Works at the **Data Link layer**
- Used for device identification within a **local** network

---

## Ports and protocols

| Term | Meaning |
| --- | --- |
| Port | A logical endpoint for communication (a number that identifies a service) |
| Protocol | Rules governing how data is transmitted and understood |

Ports + protocols together enable devices and applications to communicate reliably.

---

## TCP vs UDP

### TCP (Transmission Control Protocol)
TCP is like the **reliable post service**.

- Connection oriented (a connection is established)
- Uses a handshake (both sides agree to communicate)
- Reliable delivery (checks for errors, re-sends if needed)
- Ensures data arrives **in order**
- Supports bidirectional communication

Common uses:
- Web browsing
- Email
- File transfer

### UDP (User Datagram Protocol)
UDP is like **shouting messages quickly**.

- Connectionless (no handshake)
- Each packet is independent
- Fast, but less reliable
- Great for real time traffic

Common uses:
- Video games
- DNS
- VPNs (often uses UDP for speed, depending on implementation)

---

## OSI model

The OSI model has 7 layers and is useful because it:
- standardises how networking is understood
- makes troubleshooting easier (you can pinpoint the layer)
- allows innovation in one layer without breaking everything else

### The 7 OSI layers

| Layer | Name | What it focuses on | Examples |
| --- | --- | --- | --- |
| 7 | Application | End user network services | HTTP, FTP, SMTP, SSH, DNS |
| 6 | Presentation | Data format, encryption, compression | TLS, encryption, JPEG, MPEG |
| 5 | Session | Establishes, maintains, and ends sessions | Session management, sockets concepts |
| 4 | Transport | End to end communication | TCP, UDP |
| 3 | Network | Routing and IP packets | IP, ICMP, IPsec |
| 2 | Data Link | Frames, MAC addressing on local network | Ethernet, switches, bridges |
| 1 | Physical | Raw bits over a medium | Fibre, Wi-Fi radio, copper, hubs, repeaters |

### Layer summaries (simple)

- **Physical**: sends raw bits as signals (radio, electrical, light)
- **Data Link**: frames + MAC addresses, local delivery to next hop
- **Network**: routes packets using IP addresses
- **Transport**: reliable delivery (TCP) or fast delivery (UDP)
- **Session**: maintains the conversation between applications
- **Presentation**: data formatting, encryption, compression
- **Application**: what the user or app interacts with (HTTP, DNS, etc)

---

## TCP IP model

TCP/IP is a simpler model used in the real world.

| TCP/IP layer | Maps roughly to OSI | Examples |
| --- | --- | --- |
| Application | OSI 5 to 7 | HTTP, TLS, DNS |
| Transport | OSI 4 | TCP, UDP |
| Internet | OSI 3 | IP |
| Network access | OSI 1 to 2 | Ethernet, Wi-Fi |

---

## OSI example sender and receiver

### Example from the sender point of view
Scenario: user sends a POST request to a website using HTTPS.

| Layer | What happens |
| --- | --- |
| 7 Application | POST request created (HTTP) |
| 6 Presentation | Data is formatted, encrypted, compressed (TLS) |
| 5 Session | Session is managed (connection context) |
| 4 Transport | TCP handshake, sends to port 443 |
| 3 Network | Adds source and destination IP, creates IP packets |
| 2 Data Link | Wraps packets into frames, adds source and destination MAC |
| 1 Physical | Frames become bits and are sent as Wi-Fi radio, Ethernet electrical, or fibre light |

### Example from the receiver point of view
| Layer | What happens |
| --- | --- |
| 1 Physical | Receives the signal and converts it into bits |
| 2 Data Link | Bits assemble into frames |
| 3 Network | Frames assemble into IP packets |
| 4 Transport | Packets assemble into TCP segments and are ordered |
| 5 Session | Session is maintained |
| 6 Presentation | Decrypts and decompresses data |
| 7 Application | Web server processes the HTTP request |

---

## DNS fundamentals

DNS (Domain Name System) translates **domain names** into **IP addresses**.

Why it matters:
- humans remember names like `google.com`
- machines route traffic using IP addresses

### DNS name servers
| Type | What it does |
| --- | --- |
| Authoritative name server | Holds the actual DNS records for a domain and gives the final answer |
| Recursive resolver | Finds the answer on behalf of the client by querying other servers (and caching results) |

Zone files:
- store DNS info for a domain in a structured format
- contain DNS records

---

## DNS records

DNS records are entries in a zone file.

Common record fields:
- **Record name**: the domain being queried
- **TTL**: how long a record can be cached
- **Class**: namespace of record info (commonly IN)
- **Type**: A, AAAA, CNAME, MX, TXT, NS
- **Data**: the value (IP address, server name, text, etc)

### Common DNS record types

| Record type | What it does | Example |
| --- | --- | --- |
| A | Maps domain to IPv4 | `example.com -> 216.58.204.79` |
| AAAA | Maps domain to IPv6 | `example.com -> 2a00:1450:...` |
| CNAME | Alias one name to another | `www.example.com -> example.com` |
| MX | Mail server for a domain | `example.com -> mail.example.com` |
| TXT | Arbitrary text, often verification and SPF | `v=spf1 include:... ~all` |
| NS | Name servers hosting the zone | `ns1.provider.com` |

---

## DNS hierarchy and resolution

### DNS hierarchy
| Layer | What it does |
| --- | --- |
| Root servers | Know where top level domains live (.com, .org, etc) |
| TLD servers | Know where the authoritative name servers for domains are |
| Authoritative name servers | Hold the real DNS records for the domain |

### DNS resolution process (simple)
1. User types a domain into the browser
2. Client checks local cache and hosts file
3. Client queries a recursive DNS resolver
4. Resolver checks its cache
5. If not cached, resolver queries root servers
6. Root points resolver to the correct TLD server
7. TLD points resolver to the authoritative name server
8. Resolver asks authoritative server for the record
9. Authoritative server replies with the IP
10. Resolver caches the result and returns the IP to the client
11. Browser connects to the IP and the site loads

---

## DNS tools

### nslookup
Basic DNS query tool:
```bash
nslookup google.com
```

## dig (advanced)

`dig` is an advanced DNS query tool.

### Query a domain
```bash
dig google.com
```

### Only show the IP
```bash
dig +short google.com
```

### Show name servers
```bash
dig +short ns google.com
```

---

## The hosts file

`/etc/hosts` is a local file that maps domain names to IP addresses.

### Key behaviour
- Your machine checks `/etc/hosts` before going to DNS
- Useful for local testing or overriding DNS temporarily

### Example entry
```
127.0.0.1 example.com
```

### Edit the hosts file
```bash
sudo nano /etc/hosts
```

---

## Routing

Routing is the process of determining the best path for data to travel across networks.

Think of it like GPS for data:
- Routers use routing tables to decide where packets should go next
- Packets hop across networks until they reach the destination

### Why it matters in DevOps
- Reduces latency by choosing efficient paths
- Helps reliable application delivery
- Supports complex infrastructure (multiple networks, subnets, gateways)

### Static vs dynamic routing

| Type | What it means | Pros and cons |
| --- | --- | --- |
| Static routing | Routes are manually configured | Simple but not scalable |
| Dynamic routing | Routes update automatically | Scalable and adaptable |

### Routing protocols (examples)

| Protocol | What it is used for | Notes |
| --- | --- | --- |
| OSPF | Internal routing, shortest path | Link state, recalculates quickly |
| BGP | Routing between autonomous systems | Internet scale routing, policy based |

---

## Subnetting and CIDR

Subnetting divides a large network into smaller networks to improve management and efficiency.

### CIDR
CIDR is written as:
```
IP_address/prefix_length
```

Example:
```
192.168.1.0/24
```

### Subnet masks
Subnet masks define which part of the IP is network vs host.

Example:
`255.255.255.0` means first 24 bits are network and last 8 bits are host

---

## NAT

NAT (Network Address Translation) translates private IP addresses to public IP addresses.

### Why it exists
- Conserves public IP addresses
- Allows private networks to access the internet
- Adds a layer of network separation

### NAT process (simple)
1. Internal device uses a private IP (e.g., 192.168.1.10)
2. Router translates the source IP to a public IP (e.g., 98.117.53.254)
3. Website sees the traffic coming from the public IP
4. Response returns to the router
5. Router translates back to the correct private IP

### Types of NAT

| Type | What it does | Typical use |
| --- | --- | --- |
| Static NAT | One private IP maps to one public IP | Public facing services needing a consistent IP |
| Dynamic NAT | Private IPs map to a pool of public IPs | Public IP assigned only when needed |
| PAT | Many private IPs share one public IP using ports | Home routers, most common in households |

---

## Network troubleshooting

Network troubleshooting is important to:
- Keep systems reliable
- Identify and fix issues quickly
- Minimise downtime

### Common issues
- Connectivity loss (hardware failure, cables, configuration)
- Slow network performance
- IP address conflicts
- DNS resolution failures

### Useful commands

#### ping
Tests basic connectivity:
```bash
ping google.com
```

#### traceroute
Shows the path packets take to a destination:
```bash
traceroute google.com
```

#### nslookup
Queries DNS for domain info:
```bash
nslookup google.com
```

---

## Cloud native networking

Cloud native networking is how networking is managed inside cloud environments.

### VPC
A VPC (Virtual Private Cloud) is a private network in the cloud where you can:
- Define IP ranges
- Create subnets
- Set route tables
- Control inbound and outbound access

### Subnets
Subnets are subdivisions of a VPC, commonly split into:
- Public subnets
- Private subnets

### Gateways
Gateways connect the VPC to the outside world, handling traffic in and out:
- Internet access (public)
- Private connectivity options depending on architecture