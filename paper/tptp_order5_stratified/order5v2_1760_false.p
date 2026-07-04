% order5v2_1760  eq1=51852 eq2=45557  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,Y) = f(f(f(Z,Z),f(Y,X)),X) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(Z,f(f(f(X,X),W),W)) )).
