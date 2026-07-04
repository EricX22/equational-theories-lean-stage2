% order5v2_0360  eq1=36080 eq2=8826  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(Y,f(Z,Z)),f(Y,W)),Z) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(Y,f(Z,f(f(f(Y,Z),Y),W))) )).
