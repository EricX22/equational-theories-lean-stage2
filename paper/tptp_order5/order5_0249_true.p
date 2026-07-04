% order5_0249  eq1=8683 eq2=8933  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(Y,f(f(f(Z,W),X),Y))) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(Y,f(Z,f(f(f(Z,W),U),X))) )).
