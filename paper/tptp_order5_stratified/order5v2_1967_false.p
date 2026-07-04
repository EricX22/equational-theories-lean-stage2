% order5v2_1967  eq1=59870 eq2=60695  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(f(X,Y),Z) = f(W,f(f(Z,Z),W)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(f(X,Y),Z) != f(f(W,X),f(Z,W)) )).
