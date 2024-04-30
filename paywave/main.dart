import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:qr_code_scanner/qr_code_scanner.dart';
import 'dart:convert';

void main() {
  runApp(MyApp());
}

class PaymentSuccessPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Payment Success'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text(
              'Payment was successful!',
              style: TextStyle(fontSize: 24),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.pop(context);
              },
              child: Text('Back to Home'),
            ),
          ],
        ),
      ),
    );
  }
}

class ScanQRPage extends StatefulWidget {
  @override
  _ScanQRPageState createState() => _ScanQRPageState();
}

class _ScanQRPageState extends State<ScanQRPage> {
  final GlobalKey qrKey = GlobalKey(debugLabel: 'QR');
  QRViewController? controller;

  @override
  void reassemble() {
    super.reassemble();
    if (controller != null) {
      controller!.resumeCamera();
    }
  }

  @override
  void dispose() {
    controller?.dispose();
    super.dispose();
  }

  void _onQRViewCreated(QRViewController controller) {
    this.controller = controller;
    controller.scannedDataStream.listen((scanData) {
      _handleScannedQRCode(scanData);
    });
  }

  void _handleScannedQRCode(Barcode scanData) async {
    String? qrCodeData = scanData.code;

    final String url = 'http://127.0.0.1:5000/scan_qr'; // Replace with your server URL

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(
          <String, dynamic>{
            'qr_code': qrCodeData,
          },
        ),
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> data = json.decode(response.body);
        final String status = data['status'];

        if (status == 'success') {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Payment successful!'),
            ),
          );
          Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => PaymentSuccessPage()),
          );
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Payment failed. Please try again.'),
            ),
          );
        }
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to process QR code. Please try again.'),
          ),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('An error occurred. Please try again later.'),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Scan QR Code'),
      ),
      body: QRView(
        key: qrKey,
        onQRViewCreated: _onQRViewCreated,
      ),
    );
  }
}

class DepositMoneyPage extends StatefulWidget {
  @override
  _DepositMoneyPageState createState() => _DepositMoneyPageState();
}

class _DepositMoneyPageState extends State<DepositMoneyPage> {
  TextEditingController depositAmountController = TextEditingController();

  Future<void> depositMoney(BuildContext context) async {
    final String url = 'http://127.0.0.1:5000/deposit_money'; // Replace with your server URL

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(
          <String, dynamic>{
            'deposit_amount': double.parse(depositAmountController.text),
          },
        ),
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> data = json.decode(response.body);
        final String message = data['message'];
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(message),
          ),
        );
        Navigator.pop(context);
      } else {
        final Map<String, dynamic> data = json.decode(response.body);
        final String message = data['message'];
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(message),
          ),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('An error occurred. Please try again later.'),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Deposit Money'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: TextField(
                controller: depositAmountController,
                keyboardType: TextInputType.numberWithOptions(decimal: true),
                decoration: InputDecoration(
                  labelText: 'Enter deposit amount',
                ),
              ),
            ),
            ElevatedButton(
              onPressed: () {
                depositMoney(context);
              },
              child: Text('Deposit Money'),
            ),
          ],
        ),
      ),
    );
  }
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'PayWave App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: LoginRegisterPage(),
    );
  }
}

class LoginRegisterPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Login or Register'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => LoginPage()),
                );
              },
              child: Text('Login'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => RegisterPage()),
                );
              },
              child: Text('Register'),
            ),
          ],
        ),
      ),
    );
  }
}

class LoginPage extends StatefulWidget {
  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  TextEditingController usernameController = TextEditingController();
  TextEditingController passwordController = TextEditingController();

  Future<void> login() async {
    final String url = 'http://127.0.0.1:5000/login'; // Replace with your server URL

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(
          <String, dynamic>{
            'username': usernameController.text,
            'password': passwordController.text,
          },
        ),
      );

      if (response.statusCode == 200) {
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => HomeScreen()),
        );
      } else {
        final Map<String, dynamic> data = json.decode(response.body);
        final String message = data['message'];
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(message),
          ),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('An error occurred. Please try again later.'),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Login'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: TextField(
                controller: usernameController,
                decoration: InputDecoration(
                  labelText: 'Username',
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: TextField(
                controller: passwordController,
                obscureText: true,
                decoration: InputDecoration(
                  labelText: 'Password',
                ),
              ),
            ),
            ElevatedButton(
              onPressed: login,
              child: Text('Login'),
            ),
          ],
        ),
      ),
    );
  }
}

class RegisterPage extends StatefulWidget {
  @override
  _RegisterPageState createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  TextEditingController usernameController = TextEditingController();
  TextEditingController passwordController = TextEditingController();
  TextEditingController emailController = TextEditingController();

  Future<void> register() async {
    final String url = 'http://127.0.0.1:5000/register'; // Replace with your server URL

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(
          <String, dynamic>{
            'username': usernameController.text,
            'password': passwordController.text,
            'email': emailController.text,
          },
        ),
      );

      if (response.statusCode == 201) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Registration successful!'),
          ),
        );
      } else {
        final Map<String, dynamic> data = json.decode(response.body);
        final String message = data['message'];
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(message),
          ),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('An error occurred. Please try again later.'),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Register'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: TextField(
                controller: usernameController,
                decoration: InputDecoration(
                  labelText: 'Username',
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: TextField(
                controller: passwordController,
                obscureText: true,
                decoration: InputDecoration(
                  labelText: 'Password',
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: TextField(
                controller: emailController,
                decoration: InputDecoration(
                  labelText: 'Email',
                ),
              ),
            ),
            ElevatedButton(
              onPressed: register,
              child: Text('Register'),
            ),
          ],
        ),
      ),
    );
  }
}

class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('PayWave App'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text(
              'Welcome to PayWave!',
              style: TextStyle(fontSize: 24),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                checkBalance(context);
              },
              child: Text('Check Balance'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => ScanQRPage()),
                );
              },
              child: Text('Scan QR for Payment'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                _depositMoney(context);
              },
              child: Text('Deposit Money'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                _logout(context);
              },
              child: Text('Logout'),
            ),
          ],
        ),
      ),
    );
  }

  void _logout(BuildContext context) {
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (context) => LoginRegisterPage()),
    );
  }

  Future<void> checkBalance(BuildContext context) async {
    final String url = 'http://127.0.0.1:5000/balance'; // Replace with your server URL

    try {
      final response = await http.get(
        Uri.parse(url),
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> data = json.decode(response.body);
        final String message = data['message'];
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(message),
          ),
        );
      } else {
        final Map<String, dynamic> data = json.decode(response.body);
        final String message = data['message'];
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(message),
          ),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('An error occurred. Please try again later.'),
        ),
      );
    }
  }

  void _depositMoney(BuildContext context) {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => DepositMoneyPage()),
    );
  }
}
