% order5v2_1310  eq1=22157 eq2=37879  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(Y,f(Z,W)),f(Z,f(Z,Y))) )).
fof(neg, negated_conjecture, ? [U,V,W,X,Y,Z] : ( X != f(f(f(Y,f(Z,f(Z,W))),U),V) )).
