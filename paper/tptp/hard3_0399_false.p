% hard3_0399  eq1=4577 eq2=4625  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [U,W,X,Y,Z] : ( f(X,f(Y,Z)) = f(f(W,U),X) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(f(X,X),Y) != f(f(Z,W),Y) )).
