class Equipment:
    tag = 'equipable'
    price = 0
    description = ''
    name = ''
    bodyparts = []
    user = None

    def __str__(self):
        if self.price == 0:
            return self.name + ' - ' + self.description
        return '{} за {}'.format(self.name + ' - ' + self.description, self.price)

    def __hash__(self):
        return hash(self.name)
    
    def equip(self, user):
        self.user = user
        for part in self.bodyparts:
            self.user.equipment[part] = self
        return self
    
    def unequip(self):
        for part in self.bodyparts:
            self.user.equipment[part] = None
        self.user.inventory.append(self)
    
    def remove(self, user):
        user.inventory.remove(self)  
