% order5_0168  eq1=12402 eq2=37595  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(f(f(Z,Z),Y),f(W,W))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(Y,f(Y,f(Z,Y))),Y),Z) )).
