% order5_0161  eq1=53755 eq2=52377  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,Y) = f(f(f(f(Z,W),W),Z),Y) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(f(f(X,f(Z,Z)),W),Y) )).
