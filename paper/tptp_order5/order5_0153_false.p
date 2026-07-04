% order5_0153  eq1=16356 eq2=16969  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(f(f(X,Y),Z),X),X)) )).
fof(neg, negated_conjecture, ? [U,V,W,X,Y,Z] : ( X != f(Y,f(f(f(f(Z,W),U),V),W)) )).
