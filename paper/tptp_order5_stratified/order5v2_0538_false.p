% order5v2_0538  eq1=18203 eq2=37954  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,V,W,X,Y,Z] : ( X = f(f(Y,X),f(Z,f(f(W,U),V))) )).
fof(neg, negated_conjecture, ? [U,W,X,Y,Z] : ( X != f(f(f(Y,f(Z,f(W,Z))),U),Z) )).
