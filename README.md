# <span style="color: #ff5733;"> Obversability </span> 



## <span style="color: #33ff57;"> Containernet </span> 

First of all, we wanted to create a complete network architecture. We started Mininet but Docker is more convenient for Open Telemetry usage.
That why we used Containernet ([github](https://github.com/containernet/containernet)) which is a Mininet based project allow Docker as Host.

This section was used to create a simple example of Containernet, see below:

![containernet_example](./assets/containernet_example.webp)

### <span style="color: #5733ff;"> Run a example </span> 

**<span style="color: #ff5733;">Prerequisites</span>**

<ul style="color: #ff5733;">
    <li>Docker installed</li>
    <li>Python3 installed</li>
    <li>Containernet installed</li>
</ul>

> To install Containernet you have to follow [this official Github](https://github.com/containernet/containernet). Pay attention, bare metal installation requieres Ubuntu 18.04 !

You can run this example using the `build.sh` file inside the `containernet` folder: `sudo ./build.sh`.
> Please don't use any prefix like `sudo ./containernet/build.sh`

### <span style="color: #5733ff;"> What it does ? </span> 

When you run the `build.sh`, it first build the two Docker ([Dockerfile.pinger](./containernet/Dockerfile.pinger) and [Dockerfile.receiver](./containernet/Dockerfile.receiver)) with is just a Containernet examples update adding specific Python script ([pinger.py](./containernet/pinger.py) and [receiver.py](./containernet/receiver.py)).

> pinger.py : ping the IP `10.0.0.252` corresponding to `d2` (Docker 2)

> receiver.py : print when it is pinged by someone

Then, it run the [containernet_example.py](./containernet/containernet_example.py) using `python3 containernet_example.py`.
This one create a Mininet architecture with :
* two basic hosts (h1 and h2), 
* two dockers hosts (d1 and d2) 
* all linked by a switch (s1)

Finally, the example processes a Connectivity test between each couple of host. It shows that Dockers can ping Dockers, Hosts can ping Hosts and they can ping them together !


## <span style="color: #33ff57;"> Open Telemetry </span> 
