#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 Yesudeep Mangalapilly <yesudeep@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
:module: mom.security.codec.asn1.x509
:synopsis: ASN.1/DER decoding & encoding for X.509 certificates and public keys.

X.509 Certificate parser.
http://www.java2s.com/Open-Source/Python/Development/ASN.1-library-for-Python/pyasn1-0.0.11a/examples/x509.py.htm

Basic Certification Fields (http://tools.ietf.org/html/rfc3280#section-4.1):
----------------------------------------------------------------------------
The X.509 v3 certificate basic syntax is as follows.  For signature
calculation, the data that is to be signed is encoded using the ASN.1
distinguished encoding rules (DER) [X.690].  ASN.1 DER encoding is a
tag, length, value encoding system for each element.

ASN.1 Syntax::

    Certificate  ::=  SEQUENCE  {
        tbsCertificate       TBSCertificate,
        signatureAlgorithm   AlgorithmIdentifier,
        signatureValue       BIT STRING  }

    TBSCertificate  ::=  SEQUENCE  {
        version         [0]  EXPLICIT Version DEFAULT v1,
        serialNumber         CertificateSerialNumber,
        signature            AlgorithmIdentifier,
        issuer               Name,
        validity             Validity,
        subject              Name,
        subjectPublicKeyInfo SubjectPublicKeyInfo,
        issuerUniqueID  [1]  IMPLICIT UniqueIdentifier OPTIONAL,
                             -- If present, version MUST be v2 or v3
        subjectUniqueID [2]  IMPLICIT UniqueIdentifier OPTIONAL,
                             -- If present, version MUST be v2 or v3
        extensions      [3]  EXPLICIT Extensions OPTIONAL
                             -- If present, version MUST be v3
        }

    Version  ::=  INTEGER  {  v1(0), v2(1), v3(2)  }

    CertificateSerialNumber  ::=  INTEGER

    Validity ::= SEQUENCE {
        notBefore      Time,
        notAfter       Time }

    Time ::= CHOICE {
        utcTime        UTCTime,
        generalTime    GeneralizedTime }

    UniqueIdentifier  ::=  BIT STRING

    SubjectPublicKeyInfo  ::=  SEQUENCE  {
        algorithm            AlgorithmIdentifier,
        subjectPublicKey     BIT STRING  }

    Extensions  ::=  SEQUENCE SIZE (1..MAX) OF Extension

    Extension  ::=  SEQUENCE  {
        extnID      OBJECT IDENTIFIER,
        critical    BOOLEAN DEFAULT FALSE,
        extnValue   OCTET STRING  }
"""

from __future__ import absolute_import
from pyasn1.type import tag, namedtype, namedval, univ, constraint, char, useful

# Would be autogenerated from ASN.1 source by a ASN.1 parser
# X.509 spec (rfc2459)

MAX = 64  # TODO

class DirectoryString(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('teletexString',
                            char.TeletexString().subtype(
                                subtypeSpec=constraint.ValueSizeConstraint(
                                    1, MAX))),
        namedtype.NamedType('printableString',
                            char.PrintableString().subtype(
                                subtypeSpec=constraint.ValueSizeConstraint(
                                    1, MAX))),
        namedtype.NamedType('universalString',
                            char.UniversalString().subtype(
                                subtypeSpec=constraint.ValueSizeConstraint(
                                    1, MAX))),
        namedtype.NamedType('utf8String',
                            char.UTF8String().subtype(
                                subtypeSpec=constraint.ValueSizeConstraint(
                                    1, MAX))),
        namedtype.NamedType('bmpString',
                            char.BMPString().subtype(
                                subtypeSpec=constraint.ValueSizeConstraint(
                                    1, MAX))),
        namedtype.NamedType('ia5String',
                            char.IA5String().subtype(
                                subtypeSpec=constraint.ValueSizeConstraint(
                                    1, MAX))) # hm, this should not be here!?
        )

class AttributeValue(DirectoryString): pass

class AttributeType(univ.ObjectIdentifier): pass

class AttributeTypeAndValue(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('type', AttributeType()),
        namedtype.NamedType('value', AttributeValue())
        )

class RelativeDistinguishedName(univ.SetOf):
    componentType = AttributeTypeAndValue()

class RDNSequence(univ.SequenceOf):
    componentType = RelativeDistinguishedName()

class Name(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('', RDNSequence())
        )

class AlgorithmIdentifier(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('algorithm', univ.ObjectIdentifier()),
        namedtype.OptionalNamedType('parameters', univ.Null())
        # TODO syntax screwed?
#        namedtype.OptionalNamedType('parameters', univ.ObjectIdentifier())
        )

class Extension(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('extnID', univ.ObjectIdentifier()),
        namedtype.DefaultedNamedType('critical', univ.Boolean('False')),
        namedtype.NamedType('extnValue', univ.OctetString())
        )

class Extensions(univ.SequenceOf):
    componentType = Extension()
    sizeSpec = univ.SequenceOf.sizeSpec + constraint.ValueSizeConstraint(1, MAX)

class SubjectPublicKeyInfo(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('algorithm', AlgorithmIdentifier()),
        namedtype.NamedType('subjectPublicKey', univ.BitString())
        )


class UniqueIdentifier(univ.BitString): pass

class Time(univ.Choice):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('utcTime', useful.UTCTime()),
        namedtype.NamedType('generalTime', useful.GeneralizedTime())
        )

class Validity(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('notBefore', Time()),
        namedtype.NamedType('notAfter', Time())
        )

class CertificateSerialNumber(univ.Integer): pass

class Version(univ.Integer):
    namedValues = namedval.NamedValues(
        ('v1', 0), ('v2', 1), ('v3', 2)
        )

class TBSCertificate(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.DefaultedNamedType('version',
                                     Version('v1',
                                            tagSet=Version.tagSet.tagExplicitly(
                                                 tag.Tag(
                                                     tag.tagClassContext,
                                                     tag.tagFormatSimple, 0)))),
        namedtype.NamedType('serialNumber', CertificateSerialNumber()),
        namedtype.NamedType('signature', AlgorithmIdentifier()),
        namedtype.NamedType('issuer', Name()),
        namedtype.NamedType('validity', Validity()),
        namedtype.NamedType('subject', Name()),
        namedtype.NamedType('subjectPublicKeyInfo', SubjectPublicKeyInfo()),
        namedtype.OptionalNamedType('issuerUniqueID',
                                    UniqueIdentifier().subtype(
                                        implicitTag=tag.Tag(
                                            tag.tagClassContext,
                                            tag.tagFormatSimple, 1))),
        namedtype.OptionalNamedType('subjectUniqueID',
                                    UniqueIdentifier().subtype(
                                        implicitTag=tag.Tag(
                                            tag.tagClassContext,
                                            tag.tagFormatSimple, 2))),
        namedtype.OptionalNamedType('extensions',
                                    Extensions().subtype(
                                        explicitTag=tag.Tag(
                                            tag.tagClassContext,
                                            tag.tagFormatSimple, 3)))
        )

class Certificate(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('tbsCertificate', TBSCertificate()),
        namedtype.NamedType('signatureAlgorithm', AlgorithmIdentifier()),
        namedtype.NamedType('signatureValue', univ.BitString())
        )

# end of ASN.1 data structures
