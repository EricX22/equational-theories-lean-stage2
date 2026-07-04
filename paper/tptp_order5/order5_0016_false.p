% order5_0016  eq1=49239 eq2=30798  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,Y) = f(f(f(Z,Z),Z),f(X,Y)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(Y,f(Z,f(f(Z,X),Z))),W) )).
