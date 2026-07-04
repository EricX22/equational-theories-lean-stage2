% order5v2_1789  eq1=10636 eq2=30750  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(Y,f(f(Z,Z),f(f(Y,X),W))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(Y,f(Z,f(f(Y,Z),Y))),Z) )).
