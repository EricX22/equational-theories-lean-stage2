% order5_0098  eq1=46074 eq2=39697  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,X) = f(f(Y,Z),f(Z,f(X,X))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( X != f(f(f(f(Y,Z),f(W,Z)),Z),Y) )).
