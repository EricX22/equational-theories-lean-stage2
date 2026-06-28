% hard3_0340  eq1=3247 eq2=276  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( X = f(f(f(f(Y,Z),W),U),X) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(Y,X),Z),X) )).
