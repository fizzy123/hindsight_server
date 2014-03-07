def email_list(to_list, template_path, context_dict):
        from django.core.mail import EmailMultiAlternatives
        from django.template import loader, Context

        nodes = dict((n.name, n) for n in loader.get_template(template_path).nodelist if n.__class__.__name__ == 'BlockNode')
        con = Context(context_dict)
        r = lambda n: nodes[n].render(con)

        for address in to_list:
            msg = EmailMultiAlternatives(r('subject'), r('plain'), 'support@hindsight.com', [address,])
            msg.attach_alternative(r('html'), "text/html")
            msg.send()
            
def email(to, template_path, context_dict):
    return email_list([to,], template_path, context_dict)

def email_user(user, template_path, context_dict):
    return email_list([user.email,], template_path, context_dict)

def email_users(user_list, template_path, context_dict):
    return email_list([user.email for user in user_list], template_path, context_dict)

import math

def distance_on_unit_sphere(lat1, long1, lat2, long2):

    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
                     
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
                                            
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
                                                                
    # Compute spherical distance from spherical coordinates.
                                                                            
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
        math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc * 6373

def coordinate_range(lat, lon, dist):

    degrees_to_radians = math.pi/180.0

    phi = (90.0 - lat)*degrees_to_radians

    theta = lon*degrees_to_radians

    arc = dist/6373.0
    
    lat_range = []
    lat_range += [90.0 - (phi - arc)/degrees_to_radians]
    lat_range += [90.0 - (phi + arc)/degrees_to_radians]

    lon_range = []
    lon_range += [(theta - arc/math.cos(math.pi/2-phi))/degrees_to_radians]
    lon_range += [(theta + arc/math.cos(math.pi/2-phi))/degrees_to_radians]

    return [lat_range, lon_range]
